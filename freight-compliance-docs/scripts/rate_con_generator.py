#!/usr/bin/env python3
"""
Rate Confirmation Generator - create Rate Con PDF documents.
"""
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from shared.freight_db import get_connection

DATA_DIR = Path.home() / ".freight-broker" / "documents"


def generate_rate_con(
    carrier_name: str,
    carrier_mc: str,
    origin: str,
    destination: str,
    rate: float,
    equipment: str,
    pickup_date: str,
    load_id: str = None
) -> dict:
    """Generate Rate Confirmation PDF."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    rc_number = f"RC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    filepath = DATA_DIR / f"{rc_number}.pdf"
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        
        doc = SimpleDocTemplate(str(filepath), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        story.append(Paragraph("<b>RATE CONFIRMATION</b>", styles['Heading1']))
        story.append(Spacer(1, 10))
        
        # Header info
        story.append(Paragraph(f"<b>RC #: {rc_number}</b>", styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
        if load_id:
            story.append(Paragraph(f"Load #: {load_id}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Carrier info
        story.append(Paragraph("<b>CARRIER</b>", styles['Heading3']))
        story.append(Paragraph(f"{carrier_name}", styles['Normal']))
        story.append(Paragraph(f"MC#: {carrier_mc}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Load details table
        data = [
            ["Origin:", origin],
            ["Destination:", destination],
            ["Equipment:", equipment],
            ["Pickup Date:", pickup_date],
            ["Agreed Rate:", f"${rate:,.2f}"],
        ]
        table = Table(data, colWidths=[120, 400])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
        ]))
        story.append(table)
        story.append(Spacer(1, 30))
        
        # Terms
        story.append(Paragraph("<b>TERMS & CONDITIONS</b>", styles['Heading3']))
        terms = """Payment Terms: Net 30 days from delivery
Fuel Surcharge: Included in rate
Accessorials: As agreed
Cancellation: 24-hour notice required

By signing below, carrier confirms acceptance of this load at the agreed rate and terms."""
        story.append(Paragraph(terms, styles['Normal']))
        story.append(Spacer(1, 40))
        
        # Signature
        story.append(Paragraph("<b>CARRIER ACKNOWLEDGMENT</b>", styles['Normal']))
        story.append(Spacer(1, 20))
        story.append("I confirm acceptance of this load:")
        story.append(Spacer(1, 30))
        story.append("Signature: ________________________  Date: _______")
        story.append(Spacer(1, 10))
        story.append(f"Driver Name: ________________________")
        
        doc.build(story)
        
        return {
            "rc_number": rc_number,
            "file_path": str(filepath),
            "carrier": carrier_name,
            "rate": rate
        }
    
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate Rate Con")
    parser.add_argument("--carrier", required=True)
    parser.add_argument("--mc", required=True)
    parser.add_argument("--origin", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--rate", type=float, required=True)
    parser.add_argument("--equipment", default="Dry Van")
    parser.add_argument("--pickup", default=datetime.now().strftime('%Y-%m-%d'))
    args = parser.parse_args()
    
    result = generate_rate_con(
        args.carrier, args.mc, args.origin, args.dest,
        args.rate, args.equipment, args.pickup
    )
    
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ Rate Con generated: {result['file_path']}")
