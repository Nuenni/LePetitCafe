#!/usr/bin/env python3
"""
Ping - a tiny local web page to print a message (and optional picture) on
LePetitCafe's receipt printer from any device on the home network.

No login, no exposure beyond the home WLAN - reachable only at the Pi's
fixed local IP, e.g. http://192.168.188.43:5000
"""

import io
import logging

from flask import Flask, redirect, render_template_string, request, url_for
from PIL import Image

import printer
from receipts import ping

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__)

MAX_MESSAGE_LENGTH = 500

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LePetitCafe Ping</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --board: #26241f; --board-edge: #1c1a16; --board-dust: #332f28;
    --frame: #4a3a26; --frame-light: #6b5638;
    --chalk: #f2ede1; --chalk-dim: #cfc8b8; --chalk-faint: #8f8879;
    --paper: #f7f2e6; --paper-edge: #e7dfc9; --paper-ink: #2b271f; --paper-ink-dim: #6b6252;
    --ochre: #d7a544; --ochre-ink: #2b220a; --teal: #5c8f86;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; color: var(--chalk);
    font-family: 'Space Mono', ui-monospace, monospace;
    background: radial-gradient(ellipse at 20% 0%, var(--board-dust) 0%, transparent 55%),
                radial-gradient(ellipse at 85% 90%, var(--board-dust) 0%, transparent 50%),
                var(--board);
    padding: clamp(20px, 4vw, 56px); display: flex; justify-content: center;
  }
  .frame {
    width: 100%; max-width: 640px; border: 10px solid var(--frame); border-radius: 6px;
    box-shadow: inset 0 0 0 2px var(--frame-light), 0 30px 60px -20px rgba(0,0,0,0.6);
    padding: clamp(18px, 3vw, 34px); background: var(--board-edge);
  }
  header { text-align: center; padding-bottom: 18px; margin-bottom: 22px;
           border-bottom: 1px dashed rgba(242,237,225,0.25); }
  header .kicker { font-size: 12px; letter-spacing: 0.32em; text-transform: uppercase; color: var(--ochre); }
  header h1 { font-family: 'Caveat', cursive; font-weight: 700; font-size: clamp(46px, 12vw, 68px);
              margin: 2px 0 4px; line-height: 1; }
  header .addr { display: inline-flex; align-items: center; gap: 8px; font-size: 12px;
                 color: var(--chalk-dim); background: rgba(0,0,0,0.25);
                 border: 1px solid rgba(242,237,225,0.18); padding: 5px 14px; border-radius: 999px; }
  header .addr .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--teal);
                       box-shadow: 0 0 8px var(--teal); }
  .ticket { background: var(--paper); color: var(--paper-ink); border-radius: 3px;
            padding: 22px; }
  label { display: block; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;
          color: var(--paper-ink-dim); margin: 16px 0 6px; }
  label:first-of-type { margin-top: 0; }
  input[type=text], textarea {
    width: 100%; border: 1px solid var(--paper-edge); background: #fffdf8; color: var(--paper-ink);
    font-family: 'Space Mono', ui-monospace, monospace; padding: 12px; border-radius: 2px;
  }
  input[type=text] { font-size: 16px; }
  textarea { font-size: 20px; line-height: 1.6; min-height: 140px; resize: vertical; }
  input:focus, textarea:focus { outline: 2px solid var(--teal); outline-offset: 1px; }
  .counter { text-align: right; font-size: 11px; color: var(--paper-ink-dim); margin-top: 6px; }
  .dropzone {
    margin-top: 4px; border: 1.5px dashed var(--paper-edge); border-radius: 3px; padding: 14px;
    display: flex; align-items: center; gap: 12px; color: var(--paper-ink-dim); font-size: 13px;
    cursor: pointer;
  }
  .dropzone .icon { width: 32px; height: 32px; border-radius: 4px; background: rgba(92,143,134,0.14);
                     color: var(--teal); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
  .send-btn {
    margin-top: 22px; width: 100%; border: none; border-radius: 3px; padding: 16px;
    font-family: inherit; font-weight: 700; font-size: 15px; letter-spacing: 0.14em;
    text-transform: uppercase; background: var(--ochre); color: var(--ochre-ink); cursor: pointer;
    box-shadow: 0 10px 24px -10px rgba(215,165,68,0.55);
  }
  .flash { text-align: center; font-size: 13px; margin-top: 16px; color: var(--teal); }
  .flash.error { color: #d97757; }
</style>
</head>
<body>
  <div class="frame">
    <header>
      <div class="kicker">Le Petit Café</div>
      <h1>Ping</h1>
      <div class="addr"><span class="dot"></span>{{ address }}</div>
    </header>

    <form class="ticket" method="post" action="{{ url_for('send') }}" enctype="multipart/form-data">
      <label for="von">Von (optional)</label>
      <input type="text" id="von" name="von" maxlength="40" placeholder="z.B. Papa im Büro" value="{{ von_value }}">

      <label for="nachricht">Nachricht</label>
      <textarea id="nachricht" name="nachricht" maxlength="{{ max_len }}" required
                placeholder="Was soll auf den Bon?">{{ message_value }}</textarea>
      <div class="counter">max. {{ max_len }} Zeichen</div>

      <label for="bild">Bild (optional)</label>
      <label class="dropzone" for="bild">
        <span class="icon">▤</span>
        <span>Wird in Graustufen mitgedruckt · JPG oder PNG</span>
      </label>
      <input type="file" id="bild" name="bild" accept="image/*" style="display:none"
             onchange="this.previousElementSibling.querySelector('span:last-child').textContent = this.files[0]?.name || 'Wird in Graustufen mitgedruckt · JPG oder PNG'">

      <button class="send-btn" type="submit">An den Drucker senden ➜</button>
      {% if flash %}<div class="flash {{ flash_kind }}">{{ flash }}</div>{% endif %}
    </form>
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        PAGE,
        address=f"{request.host}",
        max_len=MAX_MESSAGE_LENGTH,
        von_value="",
        message_value="",
        flash=request.args.get("flash"),
        flash_kind=request.args.get("flash_kind", ""),
    )


@app.route("/send", methods=["POST"])
def send():
    nachricht = request.form.get("nachricht", "").strip()
    von = request.form.get("von", "").strip()
    datei = request.files.get("bild")

    if not nachricht:
        return redirect(url_for("index", flash="Bitte eine Nachricht eingeben.", flash_kind="error"))
    if len(nachricht) > MAX_MESSAGE_LENGTH:
        return redirect(url_for("index", flash="Nachricht ist zu lang.", flash_kind="error"))

    bild = None
    if datei and datei.filename:
        try:
            bild = Image.open(io.BytesIO(datei.read()))
        except Exception as exc:
            log.warning("Could not read uploaded image: %s", exc)
            return redirect(url_for("index", flash="Bild konnte nicht gelesen werden.", flash_kind="error"))

    try:
        drucker = printer.connect()
        ping.erstelle_bon(drucker, nachricht, von=von, bild=bild)
        drucker.close()
        log.info("Ping printed (von=%r, %d chars, image=%s)", von, len(nachricht), bild is not None)
    except Exception as exc:
        log.error("Ping print failed: %s", exc)
        return redirect(url_for("index", flash="Drucker nicht erreichbar.", flash_kind="error"))

    return redirect(url_for("index", flash="Gesendet!"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
