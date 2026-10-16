"""Draw the README figures from the cast data, so the pictures never drift from the lab.

Run from the repository root:  uv run tools/readme_figures.py [--png]
Writes banner.svg, cast.svg, steps.svg, session.svg and social-preview.svg in docs/assets/.
With --png it also renders social-preview.png (1280 x 640, for GitHub's social preview) with a local
Chrome or Chromium; without one it says so and leaves the PNG alone.
"""
import math
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from cast import AGENTS, GUESTS, ROOMS  # noqa: E402
from workflows import WORKFLOWS  # noqa: E402
import tomllib  # noqa: E402

CATALOGUE = ROOT / "skills" / "lab-cast" / "catalogue"
METHODS = tomllib.loads((CATALOGUE / "methods.toml").read_text(encoding="utf-8"))["persona"]
RULES = tomllib.loads((CATALOGUE / "rules.toml").read_text(encoding="utf-8"))

OUT = ROOT / "docs" / "assets"
FONT = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
GROUPS = {
    "Lead": ("#475569", ["lab-agent-pi"]),
    "Methods and code": ("#0d9488", ["lab-agent-methods", "lab-agent-engineer"]),
    "Evidence": ("#d97706", ["lab-agent-librarian", "lab-agent-factchecker", "lab-agent-referee"]),
    "Writing": ("#e11d48", ["lab-agent-editor", "lab-agent-voice"]),
}


# Short labels for the six OECD areas, in the order of rules.toml's [areas] table.
AREA_LABELS = [("Natural sciences", "#60a5fa"), ("Engineering", "#a78bfa"), ("Medicine and health", "#f472b6"),
               ("Agriculture", "#4ade80"), ("Social sciences", "#fbbf24"), ("Humanities", "#fb923c")]
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def colour(skill: str) -> str:
    return next(c for c, members in GROUPS.values() if skill in members)


def core(skill: str) -> dict:
    return next(a for a in AGENTS if a["skill"] == skill)


def guest(skill: str) -> dict:
    code, name, icon, title, _persona = next(g for g in GUESTS if g[0] == skill)
    return {"skill": code, "name": name, "icon": icon, "title": title}


def method(code: str) -> dict:
    return next(m for m in METHODS if m["code"] == code)


def initials(name: str) -> str:
    return "".join(part[0] for part in name.replace("-", " ").split()[:2])


DEFS = """<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#1e2a52"/>
    </linearGradient>
    <radialGradient id="lens" cx="0.4" cy="0.35" r="0.8">
      <stop offset="0" stop-color="#60a5fa" stop-opacity="0.45"/><stop offset="1" stop-color="#1e3a8a" stop-opacity="0.08"/>
    </radialGradient>
    <filter id="glow" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>"""


def orbit(cx: float, cy: float, rx: float, ry: float, label_size: float = 13) -> str:
    """Six research areas around a lens with a check mark: any field, one method."""
    assert len(AREA_LABELS) == len(RULES["areas"]), "AREA_LABELS must follow rules.toml [areas]"
    pts = []
    for i, (name, col) in enumerate(AREA_LABELS):
        a = -math.pi / 2 + 2 * math.pi * i / len(AREA_LABELS)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a), name, col, math.sin(a)))
    ring = " ".join(f"{x:.1f},{y:.1f}" for x, y, *_ in pts)
    out = [f'<polygon points="{ring}" fill="none" stroke="#93c5fd" stroke-opacity="0.28" stroke-width="1.2" stroke-dasharray="3 6"/>',
           f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="#93c5fd" stroke-opacity="0.22" stroke-width="1"/>']
    for x, y, name, col, sin in pts:
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{col}" stroke-opacity="0.35" stroke-width="1.2"/>')
    r = 50
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#lens)" stroke="#93c5fd" stroke-opacity="0.8" stroke-width="1.6"/>')
    gx, gy = cx - 6, cy - 6
    out.append(f'<circle cx="{gx}" cy="{gy}" r="21" fill="none" stroke="#e0f2fe" stroke-width="3.2"/>'
               f'<line x1="{gx + 15}" y1="{gy + 15}" x2="{gx + 31}" y2="{gy + 31}" stroke="#e0f2fe" stroke-width="6" stroke-linecap="round"/>'
               f'<path d="M{gx - 11},{gy + 1} l7,7 l14,-16" fill="none" stroke="#4ade80" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y, name, col, sin in pts:
        ly = y - 16 if sin < -0.9 else y + 27
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{col}" filter="url(#glow)"/>'
                   f'<text x="{x:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="{label_size}" fill="#cbd5e1">{escape(name)}</text>')
    return "\n  ".join(out)


def chips(labels: list[str], x: float, y: float, size: float = 16, per_char: float = 8.6) -> str:
    out = []
    for chip in labels:
        w = 24 + per_char * len(chip)
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{size * 2.1:.0f}" rx="{size * 1.05:.0f}" fill="#ffffff" fill-opacity="0.08" '
                   f'stroke="#93c5fd" stroke-opacity="0.45"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + size * 1.43:.0f}" text-anchor="middle" font-size="{size}" fill="#dbeafe">{escape(chip)}</text>')
        x += w + 12
    return "".join(out)


def counts() -> list[str]:
    return [f"{len(AGENTS)} core assistants", f"{len(GUESTS)} guests and guardians",
            f"{len(METHODS)} method specialists", f"{len(WORKFLOWS)} workflows"]


def banner() -> str:
    cx, cy = 1000, 160
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" font-family="{FONT}">
  {DEFS}
  <rect width="1200" height="340" rx="22" fill="url(#bg)"/>
  <g opacity="0.35" fill="#ffffff">
    <circle cx="640" cy="60" r="1.4"/><circle cx="720" cy="300" r="1.2"/><circle cx="600" cy="230" r="1"/>
    <circle cx="1170" cy="30" r="1.3"/><circle cx="1175" cy="320" r="1.1"/><circle cx="790" cy="40" r="1"/>
  </g>
  {orbit(cx, cy, 138, 104)}
  <text x="{cx}" y="326" text-anchor="middle" font-size="12.5" fill="#94a3b8">{len(RULES["areas"])} areas · {len(RULES["fos"])} fields · one method</text>
  <text x="64" y="104" font-size="62" font-weight="700" fill="#ffffff" letter-spacing="-1">Research Lab</text>
  <text x="66" y="152" font-size="28" fill="#e2e8f0">A research team inside your AI assistant.</text>
  <text x="66" y="196" font-size="18" fill="#94a3b8">It plans, searches, questions and checks.</text>
  <text x="66" y="223" font-size="18" fill="#94a3b8">You do the research and stay the author.</text>
  {chips(counts(), 64, 258)}
</svg>
'''


def cast() -> str:
    width, height = 1080, 730
    cx, cy, rx, ry = 540, 375, 330, 205
    seats = []
    n = len(AGENTS)
    for i, agent in enumerate(AGENTS):
        angle = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + rx * math.cos(angle), cy + ry * math.sin(angle)
        upper = math.sin(angle) < -0.2
        name_y, title_y = (y - 58, y - 41) if upper else (y + 52, y + 70)
        seats.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="31" fill="{colour(agent["skill"])}"/>'
            f'<text x="{x:.0f}" y="{y + 7:.0f}" text-anchor="middle" font-size="20" font-weight="700" fill="#ffffff">{escape(initials(agent["name"]))}</text>'
            f'<text x="{x:.0f}" y="{name_y:.0f}" text-anchor="middle" font-size="15" font-weight="600" fill="#0f172a">{escape(agent["short"])}</text>'
            f'<text x="{x:.0f}" y="{title_y:.0f}" text-anchor="middle" font-size="12.5" fill="#475569">{escape(agent["title"])}</text>'
        )
    legend, lx = "", 40
    for name, (col, _members) in GROUPS.items():
        legend += (f'<circle cx="{lx}" cy="34" r="7" fill="{col}"/>'
                   f'<text x="{lx + 13}" y="39" font-size="14" fill="#334155">{name}</text>')
        lx += 30 + 9 * len(name) + 22
    ids = [room["id"] for room in ROOMS]
    rooms_a, rooms_b = " · ".join(ids[:3]), " · ".join(ids[3:])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
  <rect width="{width}" height="{height}" rx="20" fill="#f8fafc" stroke="#e2e8f0"/>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx + 120}" ry="{ry + 100}" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="6 7"/>
  <text x="{cx}" y="{height - 16}" text-anchor="middle" font-size="13" fill="#64748b">dashed ring: {len(GUESTS)} guests and guardians, plus the specialists each project's classification brings in</text>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx - 95}" ry="{ry - 78}" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="2"/>
  <text x="{cx}" y="{cy - 8}" text-anchor="middle" font-size="22" font-weight="700" fill="#1e293b">The lab table</text>
  <text x="{cx}" y="{cy + 18}" text-anchor="middle" font-size="13" fill="#475569">{len(AGENTS)} core assistants · 🎓 Expert Desk for project specialists</text>
  <text x="{cx}" y="{cy + 42}" text-anchor="middle" font-size="12" fill="#64748b">rooms: {escape(rooms_a)}</text>
  <text x="{cx}" y="{cy + 59}" text-anchor="middle" font-size="12" fill="#64748b">{escape(rooms_b)}</text>
  {''.join(seats)}
  {legend}
</svg>
'''


def steps() -> str:
    """Three cards for a first project, written for researchers who do not program."""
    cards = [
        ("#0d9488", "Get the lab",
         "On this page, click Code, then Download ZIP. Unzip it into your Documents folder.",
         "Documents/ResearchLab"),
        ("#d97706", "Open a project folder",
         "Make an empty folder and open it in your AI assistant. Ask it to set the lab up; it asks before installing anything.",
         "Set up the Research Lab here"),
        ("#e11d48", "Talk to Nadia",
         "Describe your idea in plain words, in any language. Nadia classifies the project and invites its specialists.",
         "Talk to Nadia"),
    ]
    width, height, top = 1200, 330, 26
    card_w, gap, left = 350, 50, 50
    out = []
    for i, (col, title, body, prompt) in enumerate(cards):
        x = left + i * (card_w + gap)
        out.append(f'<rect x="{x}" y="{top}" width="{card_w}" height="250" rx="18" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>'
                   f'<rect x="{x}" y="{top}" width="{card_w}" height="8" rx="4" fill="{col}"/>'
                   f'<circle cx="{x + 42}" cy="{top + 54}" r="22" fill="{col}"/>'
                   f'<text x="{x + 42}" y="{top + 62}" text-anchor="middle" font-size="22" font-weight="700" fill="#ffffff">{i + 1}</text>'
                   f'<text x="{x + 78}" y="{top + 62}" font-size="21" font-weight="700" fill="#0f172a">{escape(title)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 38)):
            out.append(f'<text x="{x + 24}" y="{top + 108 + j * 23}" font-size="15.5" fill="#334155">{escape(line)}</text>')
        out.append(f'<rect x="{x + 20}" y="{top + 192}" width="{card_w - 40}" height="38" rx="10" fill="#0f172a"/>'
                   f'<text x="{x + 36}" y="{top + 216}" font-size="14" fill="#94a3b8" font-family="{MONO}">&gt;</text>'
                   f'<text x="{x + 54}" y="{top + 216}" font-size="14.5" fill="#e2e8f0" font-family="{MONO}">{escape(prompt)}</text>')
        if i < len(cards) - 1:
            ax = x + card_w + 8
            out.append(f'<path d="M{ax},{top + 125} l{gap - 22},0" stroke="#94a3b8" stroke-width="2.5"/>'
                       f'<path d="M{ax + gap - 24},{top + 117} l10,8 l-10,8" fill="none" stroke="#94a3b8" stroke-width="2.5" stroke-linejoin="round"/>')
    out.append(f'<text x="{width / 2}" y="{height - 14}" text-anchor="middle" font-size="14" fill="#64748b">'
               'No programming needed. Everything the lab writes stays in your project folder.</text>')
    body = "\n  ".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
  <rect width="{width}" height="{height}" rx="20" fill="#f8fafc" stroke="#e2e8f0"/>
  {body}
</svg>
'''


def session() -> str:
    """An illustrative first session. The cast line is cast_plan.py's real output for this profile."""
    nadia, viktor = core("lab-agent-pi"), core("lab-agent-referee")
    priya, camille = method("lab-method-causal"), method("lab-method-qualitative")
    leila, mateo = guest("lab-guest-ethics"), guest("lab-guest-dataprotection")
    width, x0, x1 = 1000, 44, 956
    out, y = [], 96

    def say(name: str, col: str, text: str) -> None:
        nonlocal y
        lines = textwrap.wrap(text, 78)
        h = 40 + 22 * len(lines)
        out.append(f'<circle cx="{x0 + 26}" cy="{y + 22}" r="20" fill="{col}"/>'
                   f'<text x="{x0 + 26}" y="{y + 28}" text-anchor="middle" font-size="15" font-weight="700" fill="#ffffff">{escape(initials(name))}</text>'
                   f'<rect x="{x0 + 58}" y="{y}" width="700" height="{h}" rx="14" fill="#f1f5f9"/>'
                   f'<text x="{x0 + 76}" y="{y + 24}" font-size="13.5" font-weight="700" fill="{col}">{escape(name)}</text>')
        for j, line in enumerate(lines):
            out.append(f'<text x="{x0 + 76}" y="{y + 48 + j * 22}" font-size="15" fill="#1e293b">{escape(line)}</text>')
        y += h + 14

    def you(text: str) -> None:
        nonlocal y
        lines = textwrap.wrap(text, 62)
        w = 36 + 8.1 * max(len(line) for line in lines)
        h = 22 + 22 * len(lines)
        out.append(f'<rect x="{x1 - 20 - w:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="14" fill="#2563eb"/>')
        for j, line in enumerate(lines):
            out.append(f'<text x="{x1 - 20 - w + 18:.0f}" y="{y + 27 + j * 22}" font-size="15" fill="#ffffff">{escape(line)}</text>')
        y += h + 14

    def panel() -> None:
        nonlocal y
        joined = [f'{priya["name"]} · causal inference', f'{camille["name"]} · qualitative methods',
                  f'{leila["name"]} · research ethics', f'{mateo["name"]} · data protection',
                  "+ new experts for household finance and financial literacy"]
        facts = ["Stories: STUDY · DATA · LIT · WRITE · DECIDE",
                 "Gate G2: ethics approval before any recruitment or data collection",
                 "Search: RePEc · SSRN · PsycINFO · ERIC · OpenAlex · Google Scholar"]
        rows, cx, cy = [], x0 + 76, y + 42
        for label in joined:
            w = 26 + 7.0 * len(label)
            if cx + w > x1 - 30:
                cx, cy = x0 + 76, cy + 36
            rows.append(f'<rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="28" rx="14" fill="#ffffff" stroke="#a7f3d0"/>'
                        f'<text x="{cx + 13:.0f}" y="{cy + 19}" font-size="13.5" fill="#065f46">{escape(label)}</text>')
            cx += w + 10
        fy = cy + 54
        for j, fact in enumerate(facts):
            rows.append(f'<text x="{x0 + 76}" y="{fy + j * 21}" font-size="13" fill="#047857">{escape(fact)}</text>')
        h = fy + 21 * (len(facts) - 1) + 18 - y
        out.append(f'<rect x="{x0 + 58}" y="{y}" width="{x1 - x0 - 78}" height="{h}" rx="14" fill="#ecfdf5" stroke="#10b981" stroke-opacity="0.6"/>'
                   f'<text x="{x0 + 76}" y="{y + 26}" font-size="13.5" font-weight="700" fill="#047857">lab-cast · joining your project</text>'
                   + "".join(rows))
        y += h + 14

    you("Talk to Nadia. I want to study how households read their credit scores.")
    say(nadia["name"], colour("lab-agent-pi"),
        "Let's classify it first, so the right people join. I read it as economics and psychology, "
        "observational and qualitative, with human participants and personal data. Is that right?")
    you("Yes, that's it.")
    panel()
    say(viktor["name"], colour("lab-agent-referee"),
        "Before anyone recruits a single household: what result would make you drop this idea?")
    say(leila["name"], "#7c3aed", "And who approves the interviews? Nothing starts until the ethics committee does.")
    height = y + 52
    body = "\n  ".join(out)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
  <rect width="{width}" height="{height}" rx="20" fill="#f8fafc"/>
  <rect x="20" y="16" width="{width - 40}" height="{height - 58}" rx="16" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
  <path d="M20,58 h{width - 40}" stroke="#e2e8f0"/>
  <circle cx="46" cy="37" r="6.5" fill="#f87171"/><circle cx="68" cy="37" r="6.5" fill="#fbbf24"/><circle cx="90" cy="37" r="6.5" fill="#4ade80"/>
  <text x="{width / 2}" y="42" text-anchor="middle" font-size="14" fill="#64748b">credit-scores · your AI assistant</text>
  {body}
  <text x="{width / 2}" y="{height - 16}" text-anchor="middle" font-size="13" fill="#64748b">Illustrative session, condensed. The specialists, stories, gate and databases are the planner's real output for this project.</text>
</svg>
'''


def social() -> str:
    """GitHub's social preview card, 1280 x 640."""
    cx, cy = 1000, 300
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640" font-family="{FONT}">
  {DEFS}
  <rect width="1280" height="640" fill="url(#bg)"/>
  <g opacity="0.35" fill="#ffffff">
    <circle cx="700" cy="80" r="1.6"/><circle cx="760" cy="560" r="1.3"/><circle cx="640" cy="420" r="1.1"/>
    <circle cx="1240" cy="50" r="1.4"/><circle cx="1230" cy="600" r="1.2"/><circle cx="820" cy="140" r="1.1"/>
  </g>
  {orbit(cx, cy, 190, 165, 17)}
  <text x="{cx}" y="560" text-anchor="middle" font-size="16" fill="#94a3b8">{len(RULES["areas"])} areas · {len(RULES["fos"])} fields · one method</text>
  <text x="80" y="210" font-size="84" font-weight="700" fill="#ffffff" letter-spacing="-1.5">Research Lab</text>
  <text x="84" y="272" font-size="32" fill="#e2e8f0">A research team inside</text>
  <text x="84" y="312" font-size="32" fill="#e2e8f0">your AI assistant.</text>
  <text x="84" y="372" font-size="22" fill="#94a3b8">It plans, searches, questions and checks.</text>
  <text x="84" y="404" font-size="22" fill="#94a3b8">You do the research and stay the author.</text>
  {chips([f"{len(AGENTS)} core assistants", f"{len(WORKFLOWS)} workflows", "any field", "MIT"], 80, 460, 18, 9.6)}
</svg>
'''


def chrome() -> str | None:
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(name):
            return shutil.which(name)
    mac = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    return str(mac) if mac.exists() else None


def render_png(svg: Path, png: Path, width: int, height: int) -> bool:
    binary = chrome()
    if binary is None:
        print("no Chrome or Chromium found; skipped the PNG")
        return False
    subprocess.run([binary, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--window-size={width},{height}", f"--screenshot={png}", svg.resolve().as_uri()],
                   check=True, capture_output=True)
    return True


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    figures = {"banner.svg": banner, "cast.svg": cast, "steps.svg": steps, "session.svg": session, "social-preview.svg": social}
    for name, draw in figures.items():
        (OUT / name).write_text(draw(), encoding="utf-8")
    print("wrote " + ", ".join(str(OUT / name) for name in figures))
    if "--png" in sys.argv[1:] and render_png(OUT / "social-preview.svg", OUT / "social-preview.png", 1280, 640):
        print(f"wrote {OUT / 'social-preview.png'}")
