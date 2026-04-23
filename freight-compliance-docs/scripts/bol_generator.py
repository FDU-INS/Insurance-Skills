#!/usr/bin/env python3
"""
BOL Generator - create Bill of Lading PDF documents.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.freight_db import get_connection

DATA_DIR = Path.home() / ".freight-broker" / "documents"


def generate_bol(
    shipper_name: str,
    shipper_address: str,
    consignee_name: str,
    consignee_address: str,
    origin: str,
    destination: str,
    commodity: str,
    weight: str,
    units: str,
    bol_number: str = None
) -> dict:
    """Generate BOL PDF."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if not bol_number:
        bol_number = f"BOL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    filepath = DATA_DIR / f"{bol_number}.pdf"
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph("<b>BILL OF LADING</b>", styles['Heading1']))
        story.append(Spacer(1, 10))
        
        # BOL Number
        story.append(Paragraph(f"<b>BOL #: {bol_number}</b>", styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Shipper / Consignee table
        data = [
            ["SHIPPER", "CONSIGNEE"],
            [f"{shipper_name}\n{shipper_address}", f"{consignee_name}\n{consignee_address}"]
        ]
        table = Table(data, colWidths=[250, 250])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Load details
        story.append(Paragraph("<b>LOAD DETAILS</b>", styles['Heading3']))
        details = [
            ["Origin:", origin],
            ["Destination:", destination],
            ["Commodity:", commodity],
            ["Weight:", f"{weight} lbs"],
            ["Units:", f"{units} pallets"],
        ]
        det_table = Table(details, colWidths=[100, 400])
        det_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(det_table)
        story.append(Spacer(1, 40))
        
        # Signature section
        story.append(Paragraph("<b>DRIVER SIGNATURE</b>", styles['Normal']))
        story.append(Spacer(1, 30))
        story.append("_" * 50)
        story.append(Spacer(1, 20))
        story.append(Paragraph("<b>RECEIVER SIGNATURE</b>", styles['Normal']))
        story.append(Spacer(1, 30))
        story.append("_" * 50)
        
        doc.build(story)
        
        return {
            "bol_number": bol_number,
            "file_path": str(filepath),
            "shipper": shipper_name,
            "destination": destination
        }
    
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate BOL")
    parser.add_argument("--shipper", required=True)
    parser.add_argument("--shipper-addr", default="")
    parser.add_argument("--consignee", required=True)
    parser.add_argument("--consignee-addr", default="")
    parser.add_argument("--origin", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--commodity", default="General Freight")
    parser.add_argument("--weight", default="20000")
    parser.add_argument("--units", default="24")
    args = parser.parse_args()
    
    result = generate_bol(
        args.shipper, args.shipper_addr,
        args.consignee, args.consignee_addr,
        args.origin, args.dest,
        args.commodity, args.weight, args.units
    )
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ BOL generated: {result['file_path']}")
