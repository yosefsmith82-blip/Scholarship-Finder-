"""Regenerate README.md from scholarships.json, sorted by deadline."""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
data = json.loads((ROOT / "scholarships.json").read_text())
today = date.fromisoformat(data["last_updated"])

PAYOUT = {"direct": "💵 To you", "school": "🏫 To school", "unconfirmed": "❓ Unconfirmed"}
CATEGORY = {
    "business": "Business",
    "business-adjacent": "Business-adjacent",
    "any-major": "Any major",
    "jewish": "Jewish students",
    "jewish-california": "Jewish + California",
}


def row(s):
    link = f"[{s['name']}]({s['url']})"
    if s["deadline"]:
        d = date.fromisoformat(s["deadline"])
        when = f"**{d.strftime('%b %-d, %Y')}**"
    else:
        when = "**Rolling / TBA**"
    note = f"<br>{s['deadline_note']}" if s.get("deadline_note") else ""
    return (
        f"| {when}{note} | {link} | {s['amount']} | {CATEGORY[s['category']]} "
        f"| {PAYOUT[s['payout']]} | {s['eligibility']} |"
    )


items = [s for s in data["scholarships"] if not s["deadline"] or date.fromisoformat(s["deadline"]) >= today]
dated = sorted((s for s in items if s["deadline"]), key=lambda s: s["deadline"])
undated = [s for s in items if not s["deadline"]]

header = "| Deadline | Scholarship (apply link) | Amount | Type | Paid to | Who can apply |\n|---|---|---|---|---|---|"

out = f"""# Scholarships for a YU Business Major from California

Last updated: **{today.strftime('%B %-d, %Y')}**. The list is sorted by deadline, soonest first, and gets re-checked every week.

For: a business major at Yeshiva University (NYC) whose home state is California. Software engineering, CS and STEM-only awards are left out.

## How the money gets paid

| Label | Meaning |
|---|---|
| 💵 To you | {data['payout_key']['direct']} |
| 🏫 To school | {data['payout_key']['school']} |
| ❓ Unconfirmed | {data['payout_key']['unconfirmed']} |

Most real scholarships send the check to your school, not to you. The awards that pay you directly are almost all essay contests and business competitions. When an award goes to your school, it pays down your YU bill first. If your account ends up with a credit balance, YU refunds the difference to you.

## Open now and upcoming (by deadline)

{header}
""" + "\n".join(row(s) for s in dated) + f"""

## Rolling or dates not posted yet

{header}
""" + "\n".join(row(s) for s in undated) + """

## Checked and left out

""" + "\n".join(f"- **{e['name']}**: {e['reason']}" for e in data["excluded"]) + """

## Scam check

A real scholarship never charges an application fee, never asks for your bank login or SSN just to apply, and never tells you that you "won" something you didn't apply to. Paid "guaranteed scholarship" services are not worth it.

## Tips

- Tell YU's Office of Student Finance about every outside award. Outside money can reduce YU's own need-based aid.
- Money you get that isn't spent on tuition, fees, books or supplies can be taxable income.
- Ask YU's Sy Syms School of Business and Office of Student Finance about their internal scholarships. They aren't posted publicly.

---
Data: [`scholarships.json`](scholarships.json). Regenerate this page with `python3 build_readme.py`.
"""

(ROOT / "README.md").write_text(out)
print(f"README.md: {len(dated)} dated, {len(undated)} rolling")
