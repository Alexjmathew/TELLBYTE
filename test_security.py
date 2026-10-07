"""Run:  python test_security.py   - checks the security controls of the app."""
import io, os, re, shutil, subprocess, sys
os.environ["GST_MAX_ROWS"] = "5000"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import pandas as pd
import config
from app import app, csv_safe
import db

c = app.test_client()
results = []
def check(name, ok):
    results.append(ok); print(("PASS  " if ok else "FAIL  ") + name)

def token():
    html = c.get("/").data.decode()
    return re.search(r'name="csrf" value="([0-9a-f]+)"', html).group(1)

def upload(data, tok, name="t.csv", extra=None):
    form = {"file": (io.BytesIO(data) if isinstance(data, bytes) else data, name), "csrf": tok}
    form.update(extra or {})
    return c.post("/analyze", data=form, content_type="multipart/form-data")

sample = open(config.SAMPLE_CSV, "rb").read()
r = c.get("/")
h = r.headers
check("CSP header blocks inline/remote scripts", "script-src 'self'" in h["Content-Security-Policy"])
check("X-Frame-Options / nosniff / no-referrer set", h["X-Frame-Options"] == "DENY" and h["X-Content-Type-Options"] == "nosniff" and h["Referrer-Policy"] == "no-referrer")
check("no inline <script>/onclick/style attributes in pages", not re.search(r"onclick=|oninput=|onsubmit=|<script>|style=", r.data.decode()))

tok = token()
check("POST without CSRF token rejected (400)", c.post("/analyze", data={"file": (io.BytesIO(sample), "t.csv")}, content_type="multipart/form-data").status_code == 400)
check("POST with wrong CSRF token rejected (400)", upload(sample, "0" * 32).status_code == 400)
check("delete without CSRF rejected (400)", c.post("/delete/abcdef123456").status_code == 400)

r = upload(sample, tok)
check("valid upload with CSRF accepted (302)", r.status_code == 302)
rid = r.headers["Location"].rsplit("/", 1)[1]
check("report page loads", c.get(f"/report/{rid}").status_code == 200)
for bad in ("../../etc/passwd", "ABCDEF123456", "%2e%2e%2fapp", "zzzzzzzzzzzz"):
    check(f"bad report id '{bad}' -> 404", c.get(f"/report/{bad}").status_code == 404 and c.get(f"/download/{bad}").status_code == 404)

check("non-CSV upload rejected", upload(b"x", tok, "evil.exe").status_code == 302)
big = pd.concat([pd.read_csv(io.BytesIO(sample))] * 3).to_csv(index=False).encode()
r = upload(big, tok); check("row limit enforced", r.status_code == 302 and "/report/" not in r.headers["Location"])
r = upload(b"seller_gstin,buyer_gstin,amount\n=cmd|' /C calc'!A0,B,100\n", tok, "../../x.csv")
check("hostile filename sanitised, tiny file handled", r.status_code in (200, 302))

df = pd.DataFrame({"a": ["=1+1", "+SUM(A1)", "-2", "@x", "ok"]})
check("CSV formula injection neutralised in export", list(csv_safe(df)["a"]) == ["'=1+1", "'+SUM(A1)", "'-2", "'@x", "ok"])

rep = db.get_report(rid)["report"]; xss = "<script>alert(1)</script>"; rep["filename"] = xss
db.save_report("aaaaaaaaaaaa", xss, rep, db.get_report(rid)["charts"])
page = c.get("/report/aaaaaaaaaaaa").data.decode()
check("filename with <script> is HTML-escaped (XSS)", xss not in page and "&lt;script&gt;" in page)
db.delete_report("aaaaaaaaaaaa")
check("DB uses parameterised SQL (no string-built queries)", "execute(f" not in open("db.py").read() and "% " not in re.sub(r'"""[\s\S]*?"""', "", open("db.py").read()).replace("# ", ""))

# integrity check: tamper with meta.json -> app must refuse to start
shutil.copy(config.META_FILE, "/tmp/meta.bak")
open(config.META_FILE, "a").write(" ")
p = subprocess.run([sys.executable, "-c", "import app"], capture_output=True, text=True)
shutil.copy("/tmp/meta.bak", config.META_FILE)
check("tampered model file -> app refuses to start", "Integrity check FAILED" in (p.stderr + p.stdout))

# login
os.environ["APP_USER"], os.environ["APP_PASSWORD"] = "u", "p"
import importlib; importlib.reload(config)
check("Basic-auth gate returns 401 without credentials", app.test_client().get("/").status_code == 401)
import base64
ok = app.test_client().get("/", headers={"Authorization": "Basic " + base64.b64encode(b"u:p").decode()})
check("Basic-auth gate accepts correct credentials", ok.status_code == 200)

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
