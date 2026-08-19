# Security Policy

## Reporting a Vulnerability

If you discover a security issue, please do **not** open a public GitHub issue.

Open a [private Security Advisory](../../security/advisories/new) directly in this repository — that creates a private space to discuss and fix it before anything is public.

This is a hobby project maintained in spare time, so there's no formal SLA, but reports will get looked at and fixed.

---

## What's actually at risk here

Le Petit Café is a receipt printer for kids. There's no user data, no accounts, no payment handling, and by design it doesn't need internet access to print — a receipt is generated and sent straight to the printer over USB/serial/local network.

The realistic attack surface is narrow:

**On the Raspberry Pi**
- `main.py` runs as an unprivileged `pi` user via systemd (see `lepetitcafe.service`), not root — it only has the supplementary `lp`/`dialout` groups needed to talk to the printer device
- The Pi needs WLAN only for SSH access during setup/maintenance, not for normal operation — standard Raspberry Pi OS hardening (change the default password, keep SSH key-only if exposed beyond the home network) applies here like on any Pi project
- `config_local.py` (real names, WLAN credentials if you add any) is gitignored and never meant to leave the device — don't commit it

**The QR-code voucher/joke pages** (`gutschein.html`, `voucher.html`, hosted via GitHub Pages)
- These are static pages with no backend. Content is looked up from `vouchers.json` by ID, or — for jokes — passed directly as a URL parameter
- User-controlled input (the `?w=` joke text, `?g=` voucher ID) is only ever written via `textContent`, never `innerHTML`, so it can't inject markup/scripts into the page
- Nothing is transmitted anywhere; the page only reads the URL it was opened with and a static JSON file

**The demo/simulator pages** (`simulator.html`, `simulator_en.html`)
- Static, generated offline by `preview.py`, no user input processed at runtime

---

## Known design decisions

| Decision | Reason |
|---|---|
| No authentication anywhere | There's nothing to protect — no accounts, no personal data beyond names you choose to put in your own gitignored `config_local.py` |
| Voucher/joke pages fetch `vouchers.json` client-side, no server | Keeps hosting to static GitHub Pages; nothing to compromise server-side |
| `main.py` runs as `pi`, not root | Standard least-privilege; only device-group membership is needed for printer access |
