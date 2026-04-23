"""SDTM Exporter.

This module provides functionality to export TrialSim data to CDISC SDTM format.

Supported export formats:
- CSV: Comma-separated values
- JSON: JavaScript Object Notation
- XPT: SAS Transport (requires pyreadstat)
"""

from __future__ import annotations

import csv
import io
import json
import logging
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Any

from trialsim.core.models import (
    AdverseEvent,
    AECausality,
    AEOutcome,
    AESeverity,
    Exposure,
    Subject,
    SubjectStatus,
    Visit,
    VisitType,
)
from trialsim.formats.sdtm.domains import (
    SDTMDomain,
    get_domain_variables,
    get_required_variables,
)

logger = logging.getLogger(__name__)


class ExportFormat(str, Enum):
    """Export file formats."""
    CSV = "csv"
    JSON = "json"
    XPT = "xpt"


@dataclass
class ExportConfig:
    """Configuration for SDTM export."""
    study_id: str = "STUDY01"
    sponsor: str = "SPONSOR"
    include_empty: bool = False
    date_format: str = "ISO8601"  # ISO8601 or SAS
    null_value: str = ""
    
    # Domain selection
    domains: list[SDTMDomain] | None = None  # None = all


@dataclass
class ExportResult:
    """Result of SDTM export operation."""
    success: bool
    domains_exported: list[SDTMDomain] = field(default_factory=list)
    record_counts: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    files_created: list[str] = field(default_factory=list)
    
    def to_summary(self) -> str:
        """Generate summary string."""
        lines = [
            "SDTM Export Summary",
            "=" * 40,
            f"Status: {'Success' if self.success else 'Failed'}",
            "",
            "Domains:",
        ]
        for domain in self.domains_exported:
            count = self.record_counts.get(domain.value, 0)
            lines.append(f"  {domain.value}: {count} records")
        
        if self.warnings:
            lines.append("")
            lines.append("Warnings:")
            for w in self.warnings[:5]:
                lines.append(f"  - {w}")
        
        if self.errors:
            lines.append("")
            lines.append("Errors:")
            for e in self.errors[:5]:
                lines.append(f"  - {e}")
        
        return "\n".join(lines)


class SDTMExporter:
    """Export TrialSim data to CDISC SDTM format.
    
    Example:
        >>> exporter = SDTMExporter()
        >>> result = exporter.export(
        ...     subjects=subjects,
        ...     adverse_events=aes,
        ...     exposures=exposures,
        ...     output_dir="/path/to/output",
        ...     format=ExportFormat.CSV,
        ... )
    """
    
    def __init__(self, config: ExportConfig | None = None):
        """Initialize exporter.
        
        Args:
            config: Export configuration
        """
        self.config = config or ExportConfig()
    
    def export(
        self,
        subjects: list[Subject] | None = None,
        visits: list[Visit] | None = None,
        adverse_events: list[AdverseEvent] | None = None,
        exposures: list[Exposure] | None = None,
        output_dir: str | Path | None = None,
        format: ExportFormat = ExportFormat.CSV,
    ) -> ExportResult:
        """Export data to SDTM format.
        
        Args:
            subjects: List of Subject records
            visits: List of Visit records
            adverse_events: List of AdverseEvent records
            exposures: List of Exposure records
            output_dir: Output directory (None for in-memory)
            format: Export file format
            
        Returns:
            ExportResult with status and details
        """
        result = ExportResult(success=True)
        
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = None
        
        # Determine domains to export
        domains = self.config.domains or [
            SDTMDomain.DM, SDTMDomain.AE, SDTMDomain.EX, SDTMDomain.SV
        ]
        
        # Export each domain
        for domain in domains:
            try:
                if domain == SDTMDomain.DM and subjects:
                    records = self._convert_dm(subjects)
                elif domain == SDTMDomain.AE and adverse_events:
                    records = self._convert_ae(adverse_events, subjects)
                elif domain == SDTMDomain.EX and exposures:
                    records = self._convert_ex(exposures, subjects)
                elif domain == SDTMDomain.SV and visits:
                    records = self._convert_sv(visits, subjects)
                else:
                    continue
                
                if records:
                    filepath = self._write_domain(
                        domain, records, output_path, format
                    )
                    result.domains_exported.append(domain)
                    result.record_counts[domain.value] = len(records)
                    if filepath:
                        result.files_created.append(str(filepath))
                        
            except Exception as e:
                result.errors.append(f"{domain.value}: {str(e)}")
                result.success = False
                logger.exception(f"Error exporting {domain.value}")
        
        return result
    
    def _convert_dm(self, subjects: list[Subject]) -> list[dict[str, Any]]:
        """Convert subjects to DM domain records."""
        records = []
        
        for subj in subjects:
            # Calculate reference dates
            ref_start = subj.screening_date or subj.randomization_date
            
            # Map arm
            arm_code = ""
            arm_desc = ""
            if subj.arm:
                arm_code = subj.arm.value.upper()
                arm_desc = subj.arm.value.replace("_", " ").title()
            
            record = {
                "STUDYID": self.config.study_id,
                "DOMAIN": "DM",
                "USUBJID": f"{self.config.study_id}-{subj.site_id}-{subj.subject_id}",
                "SUBJID": subj.subject_id,
                "SITEID": subj.site_id,
                "RFSTDTC": self._format_date(ref_start),
                "RFENDTC": "",
                "RFICDTC": self._format_date(subj.screening_date),
                "AGE": subj.age,
                "AGEU": "YEARS",
                "SEX": self._map_sex(subj.sex),
                "RACE": subj.race or "",
                "ETHNIC": subj.ethnicity or "",
                "ARMCD": arm_code,
                "ARM": arm_desc,
                "ACTARMCD": arm_code,
                "ACTARM": arm_desc,
                "COUNTRY": "USA",
                "DMDTC": self._format_date(ref_start),
            }
            records.append(record)
        
        return records
    
    def _convert_ae(
        self,
        adverse_events: list[AdverseEvent],
        subjects: list[Subject] | None = None
    ) -> list[dict[str, Any]]:
        """Convert adverse events to AE domain records."""
        # Build subject lookup
        subj_lookup = {}
        if subjects:
            for s in subjects:
                subj_lookup[s.subject_id] = s
        
        records = []
        seq_by_subj: dict[str, int] = {}
        
        for ae in adverse_events:
            # Get subject info
            subj = subj_lookup.get(ae.subject_id)
            ref_date = None
            if subj:
                ref_date = subj.randomization_date or subj.screening_date
            
            # Increment sequence
            seq = seq_by_subj.get(ae.subject_id, 0) + 1
            seq_by_subj[ae.subject_id] = seq
            
            # Build USUBJID
            site_id = subj.site_id if subj else "SITE01"
            usubjid = f"{self.config.study_id}-{site_id}-{ae.subject_id}"
            
            record = {
                "STUDYID": self.config.study_id,
                "DOMAIN": "AE",
                "USUBJID": usubjid,
                "AESEQ": seq,
                "AESPID": ae.ae_id,
                "AETERM": ae.ae_term,
                "AEDECOD": ae.ae_term,  # Would use MedDRA in production
                "AEBODSYS": ae.system_organ_class or "",
                "AESOC": ae.system_organ_class or "",
                "AESEV": self._map_severity(ae.severity),
                "AESER": "Y" if ae.is_serious else "N",
                "AEREL": self._map_causality(ae.causality),
                "AEOUT": self._map_outcome(ae.outcome),
                "AESTDTC": self._format_date(ae.onset_date),
                "AEENDTC": self._format_date(ae.resolution_date),
                "AESTDY": self._calc_study_day(ae.onset_date, ref_date),
                "AEENDY": self._calc_study_day(ae.resolution_date, ref_date),
                "AECONTRT": "Y" if ae.treatment_required else "N",
            }
            records.append(record)
        
        return records
    
    def _convert_ex(
        self,
        exposures: list[Exposure],
        subjects: list[Subject] | None = None
    ) -> list[dict[str, Any]]:
        """Convert exposures to EX domain records."""
        # Build subject lookup
        subj_lookup = {}
        if subjects:
            for s in subjects:
                subj_lookup[s.subject_id] = s
        
        records = []
        seq_by_subj: dict[str, int] = {}
        
        for exp in exposures:
            # Get subject info
            subj = subj_lookup.get(exp.subject_id)
            ref_date = None
            if subj:
                ref_date = subj.randomization_date or subj.screening_date
            
            # Increment sequence
            seq = seq_by_subj.get(exp.subject_id, 0) + 1
            seq_by_subj[exp.subject_id] = seq
            
            # Build USUBJID
            site_id = subj.site_id if subj else "SITE01"
            usubjid = f"{self.config.study_id}-{site_id}-{exp.subject_id}"
            
            record = {
                "STUDYID": self.config.study_id,
                "DOMAIN": "EX",
                "USUBJID": usubjid,
                "EXSEQ": seq,
                "EXSPID": exp.exposure_id,
                "EXTRT": exp.drug_name,
                "EXDOSE": exp.dose,
                "EXDOSU": exp.dose_unit.upper(),
                "EXROUTE": self._map_route(exp.route),
                "EXSTDTC": self._format_date(exp.start_date),
                "EXENDTC": self._format_date(exp.end_date),
                "EXSTDY": self._calc_study_day(exp.start_date, ref_date),
                "EXENDY": self._calc_study_day(exp.end_date, ref_date),
            }
            records.append(record)
        
        return records
    
    def _convert_sv(
        self,
        visits: list[Visit],
        subjects: list[Subject] | None = None
    ) -> list[dict[str, Any]]:
        """Convert visits to SV domain records."""
        # Build subject lookup
        subj_lookup = {}
        if subjects:
            for s in subjects:
                subj_lookup[s.subject_id] = s
        
        records = []
        
        for visit in visits:
            # Get subject info
            subj = subj_lookup.get(visit.subject_id)
            ref_date = None
            if subj:
                ref_date = subj.randomization_date or subj.screening_date
            
            # Build USUBJID
            site_id = visit.site_id or (subj.site_id if subj else "SITE01")
            usubjid = f"{self.config.study_id}-{site_id}-{visit.subject_id}"
            
            # Determine visit date
            visit_date = visit.actual_date or visit.planned_date
            
            record = {
                "STUDYID": self.config.study_id,
                "DOMAIN": "SV",
                "USUBJID": usubjid,
                "VISITNUM": visit.visit_number,
                "VISIT": visit.visit_name,
                "EPOCH": self._map_epoch(visit.visit_type),
                "SVSTDTC": self._format_date(visit_date),
                "SVENDTC": self._format_date(visit_date),
                "SVSTDY": self._calc_study_day(visit_date, ref_date),
            }
            
            # Add unplanned visit description
            if visit.visit_type == VisitType.UNSCHEDULED:
                record["SVUPDES"] = "Unscheduled visit"
            
            records.append(record)
        
        return records
    
    def _write_domain(
        self,
        domain: SDTMDomain,
        records: list[dict],
        output_path: Path | None,
        format: ExportFormat
    ) -> Path | None:
        """Write domain records to file.
        
        Args:
            domain: SDTM domain
            records: List of record dictionaries
            output_path: Output directory
            format: Export format
            
        Returns:
            Path to created file, or None if in-memory
        """
        if not output_path:
            return None
        
        filename = f"{domain.value.lower()}.{format.value}"
        filepath = output_path / filename
        
        if format == ExportFormat.CSV:
            self._write_csv(records, filepath)
        elif format == ExportFormat.JSON:
            self._write_json(records, filepath)
        elif format == ExportFormat.XPT:
            self._write_xpt(records, filepath, domain)
        
        return filepath
    
    def _write_csv(self, records: list[dict], filepath: Path) -> None:
        """Write records to CSV file."""
        if not records:
            return
        
        fieldnames = list(records[0].keys())
        
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
    
    def _write_json(self, records: list[dict], filepath: Path) -> None:
        """Write records to JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, default=str)
    
    def _write_xpt(
        self,
        records: list[dict],
        filepath: Path,
        domain: SDTMDomain
    ) -> None:
        """Write records to SAS XPT format."""
        try:
            import pandas as pd
            import pyreadstat
            
            df = pd.DataFrame(records)
            pyreadstat.write_xport(df, str(filepath))
        except ImportError:
            logger.warning(
                "XPT export requires pandas and pyreadstat. "
                "Falling back to CSV."
            )
            csv_path = filepath.with_suffix(".csv")
            self._write_csv(records, csv_path)
    
    # =========================================================================
    # Mapping helpers
    # =========================================================================
    
    def _format_date(self, d: date | datetime | None) -> str:
        """Format date to ISO8601."""
        if d is None:
            return ""
        if isinstance(d, datetime):
            return d.strftime("%Y-%m-%dT%H:%M:%S")
        return d.isoformat()
    
    def _calc_study_day(
        self,
        event_date: date | None,
        ref_date: date | None
    ) -> int | str:
        """Calculate study day relative to reference date."""
        if not event_date or not ref_date:
            return ""
        
        delta = (event_date - ref_date).days
        
        # SDTM convention: no day 0, day 1 is first day
        if delta >= 0:
            return delta + 1
        return delta
    
    def _map_sex(self, sex: str) -> str:
        """Map sex to SDTM codelist."""
        mapping = {
            "M": "M",
            "F": "F",
            "MALE": "M",
            "FEMALE": "F",
            "U": "U",
            "UNKNOWN": "U",
        }
        return mapping.get(sex.upper(), "U")
    
    def _map_severity(self, severity: AESeverity) -> str:
        """Map AE severity to SDTM codelist."""
        mapping = {
            AESeverity.GRADE_1: "MILD",
            AESeverity.GRADE_2: "MODERATE",
            AESeverity.GRADE_3: "SEVERE",
            AESeverity.GRADE_4: "LIFE THREATENING",
            AESeverity.GRADE_5: "FATAL",
        }
        return mapping.get(severity, "MODERATE")
    
    def _map_causality(self, causality: AECausality) -> str:
        """Map AE causality to SDTM codelist."""
        mapping = {
            AECausality.NOT_RELATED: "NOT RELATED",
            AECausality.UNLIKELY: "UNLIKELY",
            AECausality.POSSIBLY: "POSSIBLE",
            AECausality.PROBABLY: "PROBABLE",
            AECausality.DEFINITELY: "DEFINITE",
        }
        return mapping.get(causality, "POSSIBLE")
    
    def _map_outcome(self, outcome: AEOutcome) -> str:
        """Map AE outcome to SDTM codelist."""
        mapping = {
            AEOutcome.RECOVERED: "RECOVERED/RESOLVED",
            AEOutcome.RECOVERING: "RECOVERING/RESOLVING",
            AEOutcome.NOT_RECOVERED: "NOT RECOVERED/NOT RESOLVED",
            AEOutcome.RECOVERED_WITH_SEQUELAE: "RECOVERED/RESOLVED WITH SEQUELAE",
            AEOutcome.FATAL: "FATAL",
            AEOutcome.UNKNOWN: "UNKNOWN",
        }
        return mapping.get(outcome, "UNKNOWN")
    
    def _map_route(self, route: str) -> str:
        """Map route to SDTM codelist."""
        mapping = {
            "oral": "ORAL",
            "iv": "INTRAVENOUS",
            "sc": "SUBCUTANEOUS",
            "im": "INTRAMUSCULAR",
            "topical": "TOPICAL",
            "inhalation": "INHALATION",
        }
        return mapping.get(route.lower(), route.upper())
    
    def _map_epoch(self, visit_type: VisitType) -> str:
        """Map visit type to epoch."""
        mapping = {
            VisitType.SCREENING: "SCREENING",
            VisitType.BASELINE: "BASELINE",
            VisitType.RANDOMIZATION: "TREATMENT",
            VisitType.SCHEDULED: "TREATMENT",
            VisitType.UNSCHEDULED: "TREATMENT",
            VisitType.FOLLOW_UP: "FOLLOW-UP",
            VisitType.EARLY_TERMINATION: "TREATMENT",
            VisitType.END_OF_STUDY: "END OF STUDY",
        }
        return mapping.get(visit_type, "TREATMENT")


# =============================================================================
# Convenience Functions
# =============================================================================

def export_to_sdtm(
    subjects: list[Subject] | None = None,
    visits: list[Visit] | None = None,
    adverse_events: list[AdverseEvent] | None = None,
    exposures: list[Exposure] | None = None,
    output_dir: str | Path | None = None,
    format: ExportFormat = ExportFormat.CSV,
    study_id: str = "STUDY01",
) -> ExportResult:
    """Export TrialSim data to SDTM format.
    
    Args:
        subjects: List of Subject records
        visits: List of Visit records  
        adverse_events: List of AdverseEvent records
        exposures: List of Exposure records
        output_dir: Output directory
        format: Export file format
        study_id: Study identifier
        
    Returns:
        ExportResult
    """
    config = ExportConfig(study_id=study_id)
    exporter = SDTMExporter(config)
    
    return exporter.export(
        subjects=subjects,
        visits=visits,
        adverse_events=adverse_events,
        exposures=exposures,
        output_dir=output_dir,
        format=format,
    )


def create_sdtm_exporter(
    study_id: str = "STUDY01",
    sponsor: str = "SPONSOR",
) -> SDTMExporter:
    """Create an SDTM exporter with configuration.
    
    Args:
        study_id: Study identifier
        sponsor: Sponsor name
        
    Returns:
        Configured SDTMExporter
    """
    config = ExportConfig(study_id=study_id, sponsor=sponsor)
    return SDTMExporter(config)
