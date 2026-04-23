#!/usr/bin/env bash
# dispute-letter — 争议信函生成器
set -euo pipefail
CMD="${1:-help}"; shift 2>/dev/null || true; INPUT="$*"
run_python() {
python3 << 'PYEOF'
import sys
from datetime import datetime

cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
inp = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

def cmd_consumer():
    if not inp:
        print("Usage: consumer <company> <product> <issue>")
        print("Example: consumer Amazon Laptop screen-defect")
        return
    parts = inp.split()
    company = parts[0]
    product = parts[1] if len(parts) > 1 else "[Product]"
    issue = " ".join(parts[2:]) if len(parts) > 2 else "[Issue]"

    print("[Your Name]")
    print("[Your Address]")
    print("[City, State ZIP]")
    print("[Email]")
    print("")
    print("Date: {}".format(datetime.now().strftime("%B %d, %Y")))
    print("")
    print("To: {} Customer Service".format(company))
    print("[Company Address]")
    print("")
    print("RE: Complaint Regarding {} — {}".format(product, issue))
    print("")
    print("Dear Customer Service Manager,")
    print("")
    print("I am writing to formally dispute an issue with the {}".format(product))
    print("I purchased from {} on [purchase date].".format(company))
    print("")
    print("Issue: {}".format(issue))
    print("")
    print("Despite the product being within warranty/return period,")
    print("[describe what happened and previous attempts to resolve].")
    print("")
    print("I request one of the following resolutions:")
    print("  1. Full refund of $[amount]")
    print("  2. Replacement of the defective product")
    print("  3. Repair at no additional cost")
    print("")
    print("I expect a response within 14 business days. If this")
    print("matter is not resolved, I will file a complaint with")
    print("the [Consumer Protection Agency / BBB / FTC].")
    print("")
    print("Enclosed: Receipt, photos of defect, prior correspondence.")
    print("")
    print("Sincerely,")
    print("[Your Name]")

def cmd_credit():
    print("[Your Name]")
    print("[Address]")
    print("")
    print("Date: {}".format(datetime.now().strftime("%B %d, %Y")))
    print("")
    print("To: [Credit Bureau Name]")
    print("[Bureau Address]")
    print("")
    print("RE: Dispute of Inaccurate Credit Report Information")
    print("")
    print("Dear Sir/Madam,")
    print("")
    print("I am writing to dispute the following information on my")
    print("credit report (Reference #: ___). Under the Fair Credit")
    print("Reporting Act (FCRA), Section 611, I request that you")
    print("investigate and correct/remove the inaccurate items:")
    print("")
    print("  Account: [Account Name/Number]")
    print("  Reported: [What is reported]")
    print("  Correct: [What it should be]")
    print("  Reason: [Why it is inaccurate]")
    print("")
    print("I have enclosed copies of supporting documents.")
    print("Please investigate within 30 days as required by law.")
    print("")
    print("Sincerely,")
    print("[Your Name]")
    print("SSN last 4: XXXX")

def cmd_contract():
    if not inp:
        print("Usage: contract <other_party> <contract_type> <issue>")
        return
    parts = inp.split()
    party = parts[0]
    ctype = parts[1] if len(parts) > 1 else "service"
    issue = " ".join(parts[2:]) if len(parts) > 2 else "breach"

    print("[Your Name / Company]")
    print("[Address]")
    print("")
    print("Date: {}".format(datetime.now().strftime("%B %d, %Y")))
    print("")
    print("SENT VIA: Certified Mail / Email")
    print("")
    print("To: {}".format(party))
    print("[Address]")
    print("")
    print("RE: Notice of Breach of {} Contract".format(ctype.title()))
    print("Contract Date: [___]")
    print("")
    print("Dear {},".format(party))
    print("")
    print("This letter serves as formal notice that you are in")
    print("breach of our {} contract dated [___].".format(ctype))
    print("")
    print("Specifically:")
    print("  - Clause [___] requires [obligation]")
    print("  - You have failed to [specific breach]")
    print("  - This has caused [damages/impact]")
    print("")
    print("CURE PERIOD: You have [14/30] days from receipt of")
    print("this letter to cure the breach by [specific action].")
    print("")
    print("If the breach is not cured within this period, I/we")
    print("reserve the right to:")
    print("  - Terminate the contract")
    print("  - Seek damages of $[amount]")
    print("  - Pursue legal remedies")
    print("")
    print("This letter does not waive any rights under the contract.")
    print("")
    print("Sincerely,")
    print("[Your Name]")

def cmd_landlord():
    if not inp:
        print("Usage: landlord <landlord_name> <issue>")
        print("Issues: repair, deposit, noise, entry")
        return
    parts = inp.split()
    landlord = parts[0]
    issue = parts[1] if len(parts) > 1 else "repair"
    issues = {
        "repair": ("Request for Repair", "The following maintenance issue requires urgent attention:\n  - Issue: [describe]\n  - Location: [unit/area]\n  - First reported: [date]\n  - Impact on habitability: [describe]"),
        "deposit": ("Security Deposit Return", "My tenancy at [address] ended on [date].\nI request the full return of my security deposit of $[amount]\nwithin the legally required timeframe of [X] days."),
        "noise": ("Noise Complaint", "I am writing to report ongoing noise disturbance from\n[unit/source]. This has occurred on [dates/times]\nand violates the lease terms regarding quiet enjoyment."),
        "entry": ("Unauthorized Entry", "On [date], my unit was entered without the required\n[24/48]-hour written notice as required by [state] law.\nThis is a violation of my right to privacy."),
    }
    title, body = issues.get(issue, issues["repair"])

    print("[Your Name]")
    print("[Your Address]")
    print("")
    print("Date: {}".format(datetime.now().strftime("%B %d, %Y")))
    print("")
    print("To: {}".format(landlord))
    print("[Landlord Address]")
    print("")
    print("RE: {}".format(title))
    print("")
    print("Dear {},".format(landlord))
    print("")
    print(body)
    print("")
    print("Please respond within [7/14] days.")
    print("")
    print("Sincerely,")
    print("[Your Name]")

commands = {"consumer": cmd_consumer, "credit": cmd_credit, "contract": cmd_contract, "landlord": cmd_landlord}
if cmd == "help":
    print("Dispute Letter Generator")
    print("")
    print("Commands:")
    print("  consumer <co> <prod> <issue> — Consumer complaint letter")
    print("  credit                       — Credit report dispute letter")
    print("  contract <party> <type>      — Contract breach notice")
    print("  landlord <name> <issue>      — Tenant dispute (repair/deposit/noise/entry)")
elif cmd in commands:
    commands[cmd]()
else:
    print("Unknown: {}".format(cmd))
print("")
print("Powered by BytesAgain | bytesagain.com")
print("Note: Templates only. Consult a legal professional for serious disputes.")
PYEOF
}
run_python "$CMD" $INPUT
