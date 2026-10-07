# Release checklist

Status: PASS = verified in this project. `python test_security.py` re-runs the automated checks.

## 1. No hardcoding
| Item | Status | Where |
|---|---|---|
| Secret key not in code | PASS | `SECRET_KEY` env var; random per start if unset |
| Passwords / API keys / tokens in code | PASS | none exist; login uses `APP_USER` / `APP_PASSWORD` env vars |
| Paths, DB file, port, host, upload limits | PASS | `config.py` (env-overridable) |
| Detection rules and cut-offs (ITC ratio, ring length, verdict %, risk bands, approval limits) | PASS | `config.py` |
| Training settings (seed, epochs, batch size) | PASS | `config.py` |
| Dataset sizes | PASS | `python generate_dataset.py --normal N --fraud N` |
| Environment template | PASS | `.env.example` |
| Remaining constants | NOTE | model architecture (layer sizes) lives in `train_model.py`; feature list in `features.py`. These define the trained model, so they stay in code on purpose. |

## 2. No security breaching
| Control | Status |
|---|---|
| CSRF token on every POST (upload, delete) | PASS (tested) |
| Security headers: CSP (no inline/remote scripts), X-Frame-Options, nosniff, no-referrer, no-store | PASS (tested) |
| XSS: Jinja auto-escaping, no inline JS | PASS (tested with a `<script>` filename) |
| SQL injection: parameterised queries only | PASS |
| Path traversal: report ids must match `^[0-9a-f]{12}$`; filenames pass `secure_filename` | PASS (tested) |
| Upload limits: `.csv` only, 25 MB, 200,000 rows | PASS (tested) |
| CSV/formula injection in the "Flagged CSV" export | PASS (tested) |
| No pickle: scaler stored as JSON; Keras loaded with `safe_mode=True` | PASS |
| Model tamper check: SHA-256 manifest verified at start-up | PASS (tested) |
| Optional login (HTTP Basic, constant-time compare) | PASS (tested) |
| Binds to 127.0.0.1, debug off, cookies HttpOnly + SameSite=Lax | PASS |
| Data retention: `GST_RETENTION_DAYS` auto-deletes old reports; delete button on /history | PASS |
| Dependency CVEs (`pip-audit` on requirements-lock.txt) and static scan (`bandit`) | PASS after upgrading Werkzeug 3.1.7 -> 3.1.9 (CVE-2026-102598). Re-run `pip-audit` before each release: new CVEs appear over time |
| HTTPS | NOT INCLUDED: put behind nginx/Caddy with TLS before exposing beyond localhost; set `SESSION_COOKIE_SECURE` then |
| Rate limiting / multi-user accounts | NOT INCLUDED: single-user tool; add before multi-user deployment |
| Encryption at rest for the DB and `uploads/` | NOT INCLUDED: relies on disk/OS encryption; uploads contain GSTINs |

## 3. Licence issues
| Item | Status |
|---|---|
| Project licence file | ADDED: MIT. **Replace `<YOUR NAME / ORGANISATION>` in `LICENSE`, or swap the licence, before sharing.** |
| Dependency licences | PASS: all permissive (BSD-3, Apache-2.0, PSF-style). No GPL/AGPL/LGPL. See `THIRD_PARTY_LICENSES.md` |
| Nothing copied/bundled from third parties | PASS: packages are installed, not vendored; code written for this project (logic derived from your own notebook) |
| Fonts in charts | PASS: DejaVu fonts shipped with Matplotlib, permissive licence |

## 4. Third-party
| Item | Status |
|---|---|
| Versions pinned | PASS: `requirements.txt` (ranges) + `requirements-lock.txt` (exact, tested) |
| Third-party services / APIs / CDNs / analytics | PASS: none; the app makes no outbound calls and CSP blocks remote loads |
| Datasets | PASS: synthetic only, generated locally; GSTINs are fictional |
| Real taxpayer data | If you use it, you own the legal duty (IT/DPDP rules, GST confidentiality). The tool stores uploads on disk and in SQLite. |
| Pre-trained models | PASS: none downloaded; the network is trained from scratch locally |

## Known limits (not security, but be honest in reports)
- Trained on synthetic data; near-perfect scores will not carry over to real filings. Retrain on labelled real data.
- Flags are investigation leads, not proof of fraud.
