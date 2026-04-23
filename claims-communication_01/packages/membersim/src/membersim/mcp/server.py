"""MemberSim MCP Server implementation.

This module provides MCP (Model Context Protocol) tools for interacting with
MemberSim data generation capabilities. It can be used with Claude Code or
other MCP-compatible clients.

Note: Requires the 'mcp' package to be installed for server functionality.
The tool definitions can be imported without the mcp package for documentation.
"""

import json
from datetime import date
from decimal import Decimal
from typing import Any

from membersim.mcp.session import session_manager

# Tool definitions that can be used by MCP clients
TOOL_DEFINITIONS = [
    {
        "name": "create_member",
        "description": "Create a new health plan member with demographics and coverage",
        "inputSchema": {
            "type": "object",
            "properties": {
                "first_name": {"type": "string", "description": "Member first name"},
                "last_name": {"type": "string", "description": "Member last name"},
                "date_of_birth": {
                    "type": "string",
                    "description": "Birth date (YYYY-MM-DD)",
                },
                "gender": {
                    "type": "string",
                    "enum": ["M", "F"],
                    "description": "Gender",
                },
                "plan_code": {
                    "type": "string",
                    "description": "Plan code (e.g., PPO_GOLD)",
                },
                "coverage_start": {
                    "type": "string",
                    "description": "Coverage start (YYYY-MM-DD)",
                },
                "street": {"type": "string", "description": "Street address"},
                "city": {"type": "string", "description": "City"},
                "state": {"type": "string", "description": "State (2-letter)"},
                "zip_code": {"type": "string", "description": "ZIP code"},
            },
            "required": [
                "first_name",
                "last_name",
                "date_of_birth",
                "gender",
                "plan_code",
            ],
        },
    },
    {
        "name": "create_claim",
        "description": "Create a healthcare claim for a member",
        "inputSchema": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "Member ID"},
                "provider_npi": {"type": "string", "description": "Provider NPI"},
                "service_date": {
                    "type": "string",
                    "description": "Service date (YYYY-MM-DD)",
                },
                "diagnosis": {
                    "type": "string",
                    "description": "Primary diagnosis (ICD-10)",
                },
                "procedure": {
                    "type": "string",
                    "description": "Procedure code (CPT)",
                },
                "charge": {"type": "number", "description": "Charge amount"},
            },
            "required": [
                "member_id",
                "provider_npi",
                "service_date",
                "diagnosis",
                "procedure",
                "charge",
            ],
        },
    },
    {
        "name": "generate_care_gaps",
        "description": "Generate HEDIS care gaps for members",
        "inputSchema": {
            "type": "object",
            "properties": {
                "member_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Member IDs (empty for all)",
                },
                "measures": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Measure IDs (empty for all applicable)",
                },
                "gap_rate": {
                    "type": "number",
                    "description": "Target gap rate 0-1 (default 0.3)",
                },
            },
        },
    },
    {
        "name": "check_eligibility",
        "description": "Check member eligibility and generate 270/271",
        "inputSchema": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "Member ID to check"},
                "service_date": {
                    "type": "string",
                    "description": "Service date (YYYY-MM-DD)",
                },
            },
            "required": ["member_id"],
        },
    },
    {
        "name": "export_members",
        "description": "Export members in various formats",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["json", "csv", "fhir", "834"],
                    "description": "Export format",
                },
                "member_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Member IDs (empty for all)",
                },
            },
            "required": ["format"],
        },
    },
    {
        "name": "export_claims",
        "description": "Export claims in various formats",
        "inputSchema": {
            "type": "object",
            "properties": {
                "format": {
                    "type": "string",
                    "enum": ["json", "csv", "837"],
                    "description": "Export format",
                },
                "claim_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Claim IDs (empty for all)",
                },
            },
            "required": ["format"],
        },
    },
    {
        "name": "list_plans",
        "description": "List available health plan configurations",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "list_hedis_measures",
        "description": "List available HEDIS quality measures",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_member",
        "description": "Get details for a specific member",
        "inputSchema": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "Member ID"},
            },
            "required": ["member_id"],
        },
    },
    {
        "name": "list_members",
        "description": "List all members in the session",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


class MemberSimMCPHandler:
    """Handler for MemberSim MCP tool calls.

    This class provides the implementation for all MCP tools without
    requiring the mcp package. It can be used standalone or integrated
    with an MCP server.

    Uses the shared session_manager for state persistence.
    """

    def __init__(self) -> None:
        """Initialize the handler."""
        self._counter = 0

    def get_tools(self) -> list[dict[str, Any]]:
        """Get list of available tools."""
        return TOOL_DEFINITIONS

    def call_tool(self, name: str, arguments: dict[str, Any]) -> str:
        """Call a tool by name with arguments.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            JSON string result
        """
        handlers = {
            "create_member": self._create_member,
            "create_claim": self._create_claim,
            "generate_care_gaps": self._generate_care_gaps,
            "check_eligibility": self._check_eligibility,
            "export_members": self._export_members,
            "export_claims": self._export_claims,
            "list_plans": self._list_plans,
            "list_hedis_measures": self._list_hedis_measures,
            "get_member": self._get_member,
            "list_members": self._list_members,
        }

        handler = handlers.get(name)
        if not handler:
            return json.dumps({"error": f"Unknown tool: {name}"})

        try:
            return handler(arguments)
        except Exception as e:
            return json.dumps({"error": str(e)})

    def _create_member(self, args: dict[str, Any]) -> str:
        """Create a new member."""
        from healthsim.person import Address, Gender, PersonName
        from healthsim.state import Provenance

        from membersim.core.member import Member

        self._counter += 1
        member_id = f"MEM{self._counter:06d}"

        address = None
        if args.get("street"):
            address = Address(
                street=args["street"],
                city=args.get("city", ""),
                state=args.get("state", ""),
                zip_code=args.get("zip_code", ""),
            )

        coverage_start = date.fromisoformat(args.get("coverage_start", date.today().isoformat()))
        birth_date = date.fromisoformat(args["date_of_birth"])
        gender = Gender.MALE if args["gender"] == "M" else Gender.FEMALE

        member = Member(
            id=f"person-{self._counter:06d}",
            name=PersonName(given_name=args["first_name"], family_name=args["last_name"]),
            birth_date=birth_date,
            gender=gender,
            address=address,
            member_id=member_id,
            relationship_code="18",
            group_id="GRP001",
            coverage_start=coverage_start,
            plan_code=args["plan_code"],
        )

        # Add to session manager instead of local dict
        session_manager.add_member(
            member=member,
            provenance=Provenance.generated(skill="create_member"),
        )

        return json.dumps(
            {
                "member_id": member_id,
                "name": f"{args['first_name']} {args['last_name']}",
                "plan_code": args["plan_code"],
                "coverage_start": coverage_start.isoformat(),
            }
        )

    def _create_claim(self, args: dict[str, Any]) -> str:
        """Create a claim."""
        from membersim.claims.claim import Claim, ClaimLine

        member_id = args["member_id"]
        member_session = session_manager.get_by_member_id(member_id)
        if not member_session:
            return json.dumps({"error": f"Member {member_id} not found"})

        self._counter += 1
        claim_id = f"CLM{self._counter:06d}"

        line = ClaimLine(
            line_number=1,
            procedure_code=args["procedure"],
            charge_amount=Decimal(str(args["charge"])),
            units=Decimal("1"),
            service_date=date.fromisoformat(args["service_date"]),
            diagnosis_pointers=[1],
        )

        claim = Claim(
            claim_id=claim_id,
            member_id=member_id,
            subscriber_id=member_id,
            provider_npi=args["provider_npi"],
            service_date=date.fromisoformat(args["service_date"]),
            claim_type="PROFESSIONAL",
            principal_diagnosis=args["diagnosis"],
            claim_lines=[line],
        )

        # Add claim to member's session
        session_manager.add_claim(member_id, claim)

        return json.dumps(
            {
                "claim_id": claim_id,
                "member_id": member_id,
                "total_charge": float(claim.total_charge),
            }
        )

    def _generate_care_gaps(self, args: dict[str, Any]) -> str:
        """Generate care gaps."""
        from membersim.quality import generate_care_gaps

        member_ids = args.get("member_ids", [])
        measures = args.get("measures", [])
        gap_rate = args.get("gap_rate", 0.3)

        # Get members from session manager
        all_sessions = session_manager.list_all()
        members = [s.member for s in all_sessions]
        if member_ids:
            members = [m for m in members if m.member_id in member_ids]

        if not members:
            return json.dumps({"error": "No members found"})

        gaps = generate_care_gaps(
            members=members,
            measures=measures or None,
            gap_rate=gap_rate,
            measure_year=date.today().year,
        )

        return json.dumps(
            {
                "total_gaps": len(gaps),
                "gaps": [
                    {
                        "member_id": g.member_id,
                        "measure_id": g.measure_id,
                        "gap_status": g.gap_status,
                    }
                    for g in gaps
                ],
            }
        )

    def _check_eligibility(self, args: dict[str, Any]) -> str:
        """Check eligibility."""
        member_id = args["member_id"]
        member_session = session_manager.get_by_member_id(member_id)
        if not member_session:
            return json.dumps({"error": f"Member {member_id} not found"})

        member = member_session.member

        return json.dumps(
            {
                "member_id": member_id,
                "is_active": member.is_active,
                "plan_code": member.plan_code,
                "coverage_start": member.coverage_start.isoformat(),
            }
        )

    def _export_members(self, args: dict[str, Any]) -> str:
        """Export members."""
        from membersim.formats import members_to_csv, to_json

        fmt = args["format"]
        member_ids = args.get("member_ids", [])

        # Get members from session manager
        all_sessions = session_manager.list_all()
        members = [s.member for s in all_sessions]
        if member_ids:
            members = [m for m in members if m.member_id in member_ids]

        if not members:
            return json.dumps({"error": "No members to export"})

        if fmt == "json":
            return to_json(members)
        elif fmt == "csv":
            return members_to_csv(members)
        else:
            return json.dumps({"error": f"Format {fmt} not yet implemented"})

    def _export_claims(self, args: dict[str, Any]) -> str:
        """Export claims."""
        from membersim.formats import claims_to_csv, to_json

        fmt = args["format"]
        claim_ids = args.get("claim_ids", [])

        # Get all claims from session manager
        all_sessions = session_manager.list_all()
        claims = []
        for session in all_sessions:
            claims.extend(session.claims)

        if claim_ids:
            claims = [c for c in claims if c.claim_id in claim_ids]

        if not claims:
            return json.dumps({"error": "No claims to export"})

        if fmt == "json":
            return to_json(claims)
        elif fmt == "csv":
            return claims_to_csv(claims)
        else:
            return json.dumps({"error": f"Format {fmt} not yet implemented"})

    def _list_plans(self, _args: dict[str, Any]) -> str:
        """List available plans."""
        from membersim.core.plan import SAMPLE_PLANS

        plans = {
            code: {
                "plan_name": plan.plan_name,
                "plan_type": plan.plan_type,
                "deductible_individual": float(plan.deductible_individual),
                "oop_max_individual": float(plan.oop_max_individual),
            }
            for code, plan in SAMPLE_PLANS.items()
        }
        return json.dumps(plans, indent=2)

    def _list_hedis_measures(self, _args: dict[str, Any]) -> str:
        """List HEDIS measures."""
        from membersim.quality import HEDIS_MEASURES

        measures = {
            mid: {
                "name": m.measure_name,
                "ages": f"{m.min_age}-{m.max_age}",
                "gender": m.gender or "All",
            }
            for mid, m in HEDIS_MEASURES.items()
        }
        return json.dumps(measures, indent=2)

    def _get_member(self, args: dict[str, Any]) -> str:
        """Get member details."""
        from membersim.formats import to_json

        member_id = args["member_id"]
        member_session = session_manager.get_by_member_id(member_id)
        if not member_session:
            return json.dumps({"error": f"Member {member_id} not found"})
        return to_json(member_session.member)

    def _list_members(self, _args: dict[str, Any]) -> str:
        """List all members."""
        all_sessions = session_manager.list_all()
        summary = [
            {
                "member_id": s.member.member_id,
                "name": f"{s.member.name.given_name} {s.member.name.family_name}",
                "plan": s.member.plan_code,
                "claims_count": len(s.claims),
            }
            for s in all_sessions
        ]
        return json.dumps(summary, indent=2)


# Create a default handler instance
default_handler = MemberSimMCPHandler()
