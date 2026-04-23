# NetworkSim Reference Skills

Domain knowledge about healthcare network structures, benefit designs, pharmacy benefits, and regulatory standards. These skills provide background information for understanding network operations.

## Skills in This Directory

| Skill | Purpose | Key Triggers |
|-------|---------|--------------|
| [network-types.md](network-types.md) | HMO, PPO, EPO, POS network structures | "explain HMO", "network types" |
| [plan-structures.md](plan-structures.md) | Cost sharing, benefit design patterns | "deductible", "copay vs coinsurance" |
| [pharmacy-benefit-concepts.md](pharmacy-benefit-concepts.md) | PBM operations, formulary, tier structures | "formulary tiers", "PBM" |
| [network-adequacy.md](network-adequacy.md) | CMS/NCQA access standards | "adequacy standards", "time distance" |
| [pbm-operations.md](pbm-operations.md) | Claims processing, rebates, MAC pricing | "BIN PCN", "rebates" |
| [specialty-pharmacy.md](specialty-pharmacy.md) | Limited distribution, hub models, REMS | "specialty drugs", "hub services" |
| [utilization-management.md](utilization-management.md) | Prior auth, step therapy, quantity limits | "prior auth", "step therapy" |

## Network Type Comparison

| Type | Network Access | Referrals | Out-of-Network | Cost |
|------|---------------|-----------|----------------|------|
| HMO | Closed - in-network only | Required | Emergency only | Lowest |
| PPO | Open - any provider | Not required | Higher cost share | Higher |
| EPO | Closed - in-network only | Not required | Emergency only | Moderate |
| POS | Hybrid | For specialists | Available | Moderate |

## Formulary Tier Structure

| Tier | Drug Type | Typical Copay |
|------|-----------|---------------|
| 1 | Generic | $10-15 |
| 2 | Preferred Brand | $30-50 |
| 3 | Non-Preferred Brand | $60-80 |
| 4 | Specialty | 20-30% coinsurance |

## Utilization Management Programs

| Program | Purpose | Common Applications |
|---------|---------|---------------------|
| Prior Authorization | Medical necessity review | Specialty drugs, imaging, surgery |
| Step Therapy | Try preferred options first | Biologics, specialty medications |
| Quantity Limits | Prevent overutilization | Controlled substances, high-cost drugs |

## Regulatory Context

Reference skills provide context for understanding:
- Why networks have access standards (CMS MA requirements)
- How formularies are structured (clinical + cost optimization)
- What triggers utilization management (safety + cost)
- How pharmacy benefits flow through PBMs

## Related Skills

- [Query Skills](../query/) - Search actual provider data
- [Analytics Skills](../analytics/) - Apply standards to real networks
- [Synthetic Skills](../synthetic/) - Generate entities using these patterns
- [Pattern Skills](../patterns/) - Network configuration templates

---

*Reference skills explain "how things work" in healthcare networks - use them for education and context.*
