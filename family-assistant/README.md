# Family Assistant Skill for Claude

A ready-to-use skill template that turns Claude into your family's personal assistant — one who already knows your insurance policy numbers, your kids' allergies, your accountant's phone number, and which airline loyalty program to use when booking flights.

## What This Is

This is a **skill** for [Claude](https://claude.ai) (works with both [Cowork](https://claude.ai) and [Claude Code](https://docs.claude.com/en/docs/claude-code)). Once you fill in your family's information, Claude can:

- **Fill out forms** — medical intake, school enrollment, insurance claims, government paperwork, travel documents
- **Handle insurance** — look up your policy numbers, draft claim letters, reference copays and deductibles
- **Manage medical info** — know your kids' allergies, current medications, provider contacts, and upcoming appointments
- **Book travel** — apply the right loyalty program numbers, seat preferences, TSA PreCheck, and passport details
- **Coordinate household logistics** — contractor contacts, utility accounts, vehicle info, service schedules
- **Assist with finances** — route to the right bank account, connect you with your CPA, reference recurring bills

Instead of hunting through filing cabinets, email, or your phone's notes app every time you need a policy number or your kid's pediatrician's fax number, you just ask Claude.

## Why This Works Well

The skill uses a **modular reference file design** — Claude only loads the information it needs for a given task. Ask it to fill out a school health form? It pulls up `family-members.md` and `medical.md`. Need to file an insurance claim? It grabs `insurance.md` and `medical.md`. This keeps things fast and focused.

The skill also instructs Claude to be **privacy-conscious** (only showing last 4 digits of sensitive numbers) and **proactive** (e.g., flagging a child's nut allergy when filling out a camp form you might have overlooked).

## Getting Started

### 1. Copy this template into your skills directory

**For Cowork users:**
Drop the `family-assistant-template` folder into whichever folder you select when starting a Cowork session. Rename it to something like `my-family-assistant`.

**For Claude Code users:**
Copy it into your skills directory:
```bash
cp -r family-assistant-template ~/.claude/skills/my-family-assistant
```

### 2. Rename the skill

Open `SKILL.md` and replace the placeholders:
- `[YOUR LAST NAME]` → your family name
- `[YOUR NAME]` → your first name
- Update the `name:` field in the YAML header (e.g., `name: johnson-family-assistant`)

### 3. Fill in your reference files

Work through each file in the `references/` folder. You don't need to fill everything in at once — start with what you use most:

| File | What to fill in | Start here if you... |
|------|----------------|---------------------|
| `family-members.md` | Names, DOBs, contact info, IDs | Fill out any kind of forms regularly |
| `medical.md` | Allergies, medications, doctors | Have kids with allergies or ongoing prescriptions |
| `insurance.md` | Policy numbers, coverage details | Deal with insurance claims or benefits questions |
| `household.md` | Address, utilities, contractors | Manage a household with service providers |
| `preferences.md` | Loyalty programs, travel docs, dietary needs | Travel frequently or book reservations |
| `finance.md` | Bank accounts, advisors, recurring bills | Handle financial paperwork or tax prep |

Each file has **comments and placeholder tables** — just fill in the blanks. Delete any sections that don't apply to your situation (no second home? remove that section). Add new sections if you need them.

### 4. Start using it

Once your files are in place, Claude will automatically recognize the skill. Try things like:

- *"Fill out this school enrollment form for my daughter"*
- *"What's our dental insurance group number?"*
- *"I need to schedule an appointment with the allergist — what's their number?"*
- *"Book a flight to Chicago — use my preferred airline and loyalty number"*
- *"Draft an insurance appeal for the denied claim from last month"*
- *"What's our accountant's email? I need to send over tax documents"*

## File Structure

```
family-assistant-template/
├── SKILL.md                          # Main skill definition + workflows
├── README.md                         # This file
└── references/
    ├── family-members.md             # Identity, contacts, IDs, emergency contacts
    ├── insurance.md                  # Health, dental, vision, auto, home, life
    ├── medical.md                    # Allergies, medications, providers, pharmacy
    ├── household.md                  # Address, utilities, services, vehicles
    ├── preferences.md                # Travel, dining, scheduling, birthdays
    └── finance.md                    # Accounts, cards, advisors, taxes, bills
```

## Tips

**Start small.** You don't need to fill in every field on day one. Start with the file you'd use most — for many families, that's `family-members.md` and `medical.md` — and expand over time.

**Keep it updated.** When you switch insurance plans, get a new doctor, or renew a passport, update the relevant reference file. A quick edit now saves you 20 minutes of searching later.

**Use it with browser tools.** In Cowork, Claude can use the browser to actually fill in web forms on your behalf. Combined with this skill, it becomes remarkably capable at handling online paperwork.

**Add your own sections.** The template covers common scenarios, but every family is different. Have a boat? Add a marine insurance section. Homeschool your kids? Add a curriculum section. The structure is just markdown — easy to extend.

**Privacy note.** These files live locally on your machine (or wherever you store your skills folder). Claude loads them on-demand during a session. Use the "last 4 digits" convention for sensitive numbers, and never put full passwords in these files.

## How Skills Work

Skills are a feature of Claude Code and Cowork that give Claude persistent, specialized knowledge. A skill is just a folder with a `SKILL.md` file (the instructions) and optional reference files (the data). When Claude encounters a task that matches a skill's triggers, it loads the relevant instructions and files.

For more on building skills: [Claude Code documentation](https://docs.claude.com)

## Background

This template was built by [Eric Porres](https://github.com/ericporres) after creating a personal family assistant skill for daily use with Claude. The original handles everything from filling out school forms for four kids to coordinating insurance claims across multiple providers. This template abstracts that into a blank starting point anyone can customize.

## License

MIT — use it however you'd like.
