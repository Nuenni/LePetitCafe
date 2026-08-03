#!/usr/bin/env python3
"""
LePetitCafe Web-Simulator — Bons im Browser testen, ohne Hardware.

Starten:  python3 simulate_web.py
Öffnen:   http://localhost:5000
"""

import sys, os, json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import webbrowser, threading

sys.path.insert(0, os.path.dirname(__file__))
from receipts import supermarkt, eiscafe, restaurant

# ── Mock-Drucker → HTML ────────────────────────────────────────────────────────

class HtmlPrinter:
    def __init__(self):
        self._bold = False
        self._big  = False
        self._align = "left"
        self.blocks: list[dict] = []

    def set(self, bold=None, double_height=None, double_width=None, align=None, **_):
        if bold          is not None: self._bold  = bold
        if double_height is not None: self._big   = double_height
        if align         is not None: self._align = align

    def text(self, txt: str):
        lines = txt.split("\n")
        # Ein abschliessendes \n beendet nur die Zeile, es ist keine Leerzeile.
        if lines and lines[-1] == "":
            lines.pop()
        for line in lines:
            self.blocks.append({
                "t": line, "b": self._bold or self._big,
                "big": self._big, "a": self._align,
            })

    def cut(self):
        self.blocks.append({"cut": True})

    def close(self): pass

    def to_html(self) -> str:
        rows = []
        for bl in self.blocks:
            if bl.get("cut"):
                rows.append('<hr class="cut">')
                continue
            txt   = bl["t"].replace("&","&amp;").replace("<","&lt;")
            cls   = []
            if bl["b"]:   cls.append("bold")
            if bl["big"]: cls.append("big")
            if bl["a"] == "center": cls.append("center")
            if bl["a"] == "right":  cls.append("right")
            c = f' class="{" ".join(cls)}"' if cls else ""
            rows.append(f"<div{c}>{txt or '&nbsp;'}</div>")
        return "\n".join(rows)


WELTEN = {
    "supermarkt": ("PETIT MARCHÉ",   supermarkt.erstelle_bon,  "#c0392b"),
    "eiscafe":    ("LE PETIT CAFÉ",  eiscafe.erstelle_bon,     "#8e44ad"),
    "restaurant": ("LE PETIT BISTRO",restaurant.erstelle_bon,  "#1a5276"),
}

def generate(key: str) -> dict:
    name, fn, accent = WELTEN[key]
    p = HtmlPrinter()
    fn(p)
    return {"name": name, "accent": accent, "html": p.to_html()}


# ── HTTP-Handler ───────────────────────────────────────────────────────────────

PAGE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>LePetitCafe Simulator</title>
<style>
* { box-sizing:border-box; margin:0; padding:0; }
body {
  background: #1e1e1e;
  font-family: 'Segoe UI', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 16px 60px;
  gap: 32px;
}

h1 {
  color: #fff;
  font-size: 1rem;
  letter-spacing: 4px;
  text-transform: uppercase;
  opacity: .4;
}

/* ── Buttons ── */
.buttons {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}
.btn {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  font-family: 'Segoe UI', sans-serif;
  font-size: .75rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #fff;
  box-shadow: 0 6px 0 rgba(0,0,0,.4), 0 8px 20px rgba(0,0,0,.5);
  transition: transform .08s, box-shadow .08s;
  position: relative;
  top: 0;
}
.btn:active {
  transform: translateY(4px);
  box-shadow: 0 2px 0 rgba(0,0,0,.4), 0 4px 10px rgba(0,0,0,.3);
  top: 4px;
}
.btn-supermarkt  { background: #c0392b; }
.btn-eiscafe     { background: #8e44ad; }
.btn-restaurant  { background: #1a5276; }

/* ── Receipt ── */
.stage {
  perspective: 800px;
}
.receipt-wrap {
  animation: popIn .35s cubic-bezier(.22,1,.36,1);
}
@keyframes popIn {
  from { opacity:0; transform: translateY(-30px) scale(.96); }
  to   { opacity:1; transform: translateY(0)     scale(1);   }
}

.receipt {
  width: 320px;
  background: #faf6ee;
  padding: 32px 22px 40px;
  box-shadow: 0 4px 8px rgba(0,0,0,.3), 0 16px 40px rgba(0,0,0,.4);
  clip-path: polygon(
    0% 0%,   3% 1.2%, 6% 0%,  9% 1.2%, 12% 0%, 15% 1.2%, 18% 0%,
    21% 1.2%,24% 0%, 27% 1.2%,30% 0%, 33% 1.2%,36% 0%, 39% 1.2%,
    42% 0%, 45% 1.2%,48% 0%, 51% 1.2%,54% 0%, 57% 1.2%,60% 0%,
    63% 1.2%,66% 0%, 69% 1.2%,72% 0%, 75% 1.2%,78% 0%, 81% 1.2%,
    84% 0%, 87% 1.2%,90% 0%, 93% 1.2%,96% 0%, 100% 0%,
    100% 98.5%, 97% 100%, 94% 98.5%, 91% 100%, 88% 98.5%, 85% 100%,
    82% 98.5%, 79% 100%, 76% 98.5%, 73% 100%, 70% 98.5%, 67% 100%,
    64% 98.5%, 61% 100%, 58% 98.5%, 55% 100%, 52% 98.5%, 49% 100%,
    46% 98.5%, 43% 100%, 40% 98.5%, 37% 100%, 34% 98.5%, 31% 100%,
    28% 98.5%, 25% 100%, 22% 98.5%, 19% 100%, 16% 98.5%, 13% 100%,
    10% 98.5%,  7% 100%,  4% 98.5%,  1% 100%,  0% 98.5%
  );
  position: relative;
}
.receipt::before {
  content:'';
  position:absolute;
  inset:0;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 3px,
    rgba(0,0,0,.012) 3px, rgba(0,0,0,.012) 4px
  );
  pointer-events:none;
}

/* ── Receipt typography ── */
.receipt div {
  font-family: 'Courier New', Courier, monospace;
  font-size: .72rem;
  line-height: 1.65;
  color: #222;
  white-space: pre;
  min-height: 1.1em;
}
.receipt div.bold   { font-weight: 700; }
.receipt div.big    { font-size: 1rem; font-weight: 700; }
.receipt div.center { text-align: center; }
.receipt div.right  { text-align: right; }
.receipt hr.cut {
  border: none;
  border-top: 1px dashed #bbb;
  margin: 8px 0;
}

/* ── hint ── */
.hint {
  color: #ffffff30;
  font-size: .7rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-align: center;
}
</style>
</head>
<body>
<h1>LePetitCafe Simulator</h1>

<div class="buttons">
  <button class="btn btn-supermarkt" onclick="print('supermarkt')">🛒<br>Super<br>markt</button>
  <button class="btn btn-eiscafe"    onclick="print('eiscafe')"   >🍦<br>Eis<br>café</button>
  <button class="btn btn-restaurant" onclick="print('restaurant')">🍽️<br>Res<br>taurant</button>
</div>

<div class="stage">
  <div id="out"></div>
</div>

<p class="hint">Knopf drücken → Bon erscheint</p>

<script>
async function print(type) {
  const res  = await fetch('/bon/' + type);
  const data = await res.json();
  const out  = document.getElementById('out');

  // Accent-Farbe für Ladenname
  document.documentElement.style.setProperty('--accent', data.accent);

  out.innerHTML = `
    <div class="receipt-wrap">
      <div class="receipt" style="--accent:${data.accent}">
        ${data.html}
      </div>
    </div>`;

  // Ladenname einfärben (erstes .big-Element)
  const first = out.querySelector('.big');
  if (first) first.style.color = data.accent;

  out.scrollIntoView({behavior:'smooth', block:'nearest'});
}
</script>
</body>
</html>
"""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass  # kein Request-Log im Terminal

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/":
            self._respond(200, "text/html", PAGE.encode())

        elif path.startswith("/bon/"):
            key = path.split("/bon/")[-1]
            if key not in WELTEN:
                self._respond(404, "text/plain", b"Not found")
                return
            data = generate(key)
            self._respond(200, "application/json", json.dumps(data).encode())

        else:
            self._respond(404, "text/plain", b"Not found")

    def _respond(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)


# ── Start ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = 5000
    url  = f"http://localhost:{port}"

    try:
        server = HTTPServer(("", port), Handler)
    except OSError:
        print(f"\n  Port {port} ist bereits belegt.")
        print(f"  Anderen Port angeben: python3 simulate_web.py 5001\n")
        sys.exit(1)

    if len(sys.argv) > 1:
        try:
            port   = int(sys.argv[1])
            url    = f"http://localhost:{port}"
            server = HTTPServer(("", port), Handler)
        except (ValueError, OSError) as e:
            print(f"Fehler: {e}")
            sys.exit(1)

    print(f"\n  LePetitCafe Simulator läuft!")
    print(f"  ════════════════════════════")
    print(f"  Jetzt im Browser öffnen:")
    print(f"\n      {url}\n")
    print(f"  Strg+C zum Beenden\n")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Tschüss!")
