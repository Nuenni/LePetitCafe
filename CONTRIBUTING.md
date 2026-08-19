# Contributing to Le Petit Café

Thanks for your interest in contributing! This is a small hobby project, but PRs, bug reports, and ideas are genuinely welcome — new play worlds, new languages, hardware/enclosure ideas, bug fixes.

---

## Getting started

You don't need the hardware to contribute. Most of this repo is pure Python and can be tested on any machine:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. `pip3 install python-escpos pyusb` (RPi.GPIO is only needed to actually run `main.py` on a Pi)
4. Make your changes
5. Run the test suite: `python3 test_receipts.py`
6. If you touched a receipt generator, regenerate the demo pages: `python3 preview.py`
7. Push your branch and open a pull request

If you have a real ESC/POS printer, `test_local_printer.py` lets you print over USB directly from your own computer (Mac/Linux) — no Pi needed. See the docstring at the top of that file for setup.

---

## Opening issues

For non-trivial changes, open an issue first to describe what you want to build or fix — avoids duplicate work and lets us align early.

For bug reports, include:
- What you expected to happen
- What actually happened
- Your environment (OS, Python version, printer model if hardware-related)

Security issues should **not** be reported as public issues — see [SECURITY.md](SECURITY.md).

---

## Pull request guidelines

- One feature or fix per PR — keep changes focused
- Link the issue in the PR description (`Closes #123`) if there is one
- Run `python3 test_receipts.py` before pushing — it checks that every receipt fits the paper width at 48/42/32 columns
- If you add or change QR/barcode content, keep it plain ASCII (see the note in `receipts/layout.py::codes`) — accented characters behave unpredictably once the printer encodes the QR code natively
- Keep commit messages clear and in the imperative: "Add bakery play world" not "Added bakery stuff"

---

## Adding a new play world

Each play world (Supermarket, Ice Cream Café, Restaurant, ...) is one file under `receipts/`, in both German and English (e.g. `supermarkt.py` / `supermarket.py`). A new world should:

- Follow the existing structure: a menu/item list, an `erstelle_bon()`/`create_receipt()` function using the shared helpers in `receipts/layout.py`
- Come in both languages, with matching filenames per the existing DE/EN pairs
- Add a few short jokes for the QR code fallback (see `JOKES`/`WITZE` in any existing file)
- Get wired up in `main.py` (button mapping) — see `config.py` for the `GPIO_*` pins

Vouchers that show up on the receipt's QR code are **not** hardcoded per world — they come from the shared pool in `vouchers.json` (used by `layout.voucher_url()`). Add new voucher ideas there instead of duplicating them per world.

---

## Adding a language

Translate an existing pair of files (e.g. `eiscafe.py` → `icecream.py`) and add the new module names to the `if config.LANGUAGE == "..."` blocks in `main.py`, `test_local_printer.py`, and `preview.py`. Add matching `de`/`en`-style keys to `vouchers.json` for the voucher/joke pages, and a `gutschein.html`-style landing page for the new language if you want vouchers to render nicely rather than fall back to raw text.

---

## Code style

- No new comments explaining *what* code does — only add a comment for a non-obvious constraint or workaround (see the existing comments in `receipts/layout.py` for the tone to match)
- Match the existing German-language code comments in German files and English comments in English files
- Never put real names into anything that gets committed — see the disclaimer in `README.md`
