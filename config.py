"""All tunable settings in ONE place. Every value can be overridden with an environment variable
(or a .env-style export) so nothing needs editing in the code."""
import os


def _int(name, default):
    return int(os.environ.get(name, default))


def _float(name, default):
    return float(os.environ.get(name, default))


# ---- paths -----------------------------------------------------------------
DATA_DIR = os.environ.get("GST_DATA_DIR", "data")
MODEL_DIR = os.environ.get("GST_MODEL_DIR", "model")
UPLOAD_DIR = os.environ.get("GST_UPLOAD_DIR", "uploads")
DB_PATH = os.environ.get("GST_DB_PATH", os.path.join(DATA_DIR, "gst_reports.db"))
SAMPLE_CSV = os.path.join(DATA_DIR, "transactions.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "gst_nn.keras")
SCALER_FILE = os.path.join(MODEL_DIR, "scaler.json")
META_FILE = os.path.join(MODEL_DIR, "meta.json")
MANIFEST_FILE = os.path.join(MODEL_DIR, "manifest.json")      # SHA-256 of model files

# ---- server / security -----------------------------------------------------
HOST = os.environ.get("GST_HOST", "127.0.0.1")                # local only by default
PORT = _int("GST_PORT", 5000)
SECRET_KEY = os.environ.get("SECRET_KEY")                     # set in production; random if missing
APP_USER = os.environ.get("APP_USER")                         # set both to require a login
APP_PASSWORD = os.environ.get("APP_PASSWORD")
MAX_UPLOAD_MB = _int("GST_MAX_UPLOAD_MB", 25)
MAX_ROWS = _int("GST_MAX_ROWS", 200_000)
RETENTION_DAYS = _int("GST_RETENTION_DAYS", 0)                # 0 = keep forever; N = auto-delete older

# ---- detection settings ----------------------------------------------------
DEFAULT_THRESHOLD = _float("GST_THRESHOLD", 0.5)
THRESHOLD_MIN, THRESHOLD_MAX = 0.05, 0.95
HIGH_RISK_PROB = _float("GST_HIGH_RISK_PROB", 0.8)
APPROVAL_THRESHOLDS = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000]   # INR approval limits
NEAR_THRESHOLD_BAND = 0.05                                    # "just below" = within 5%
DEFAULT_SELLER_AGE_DAYS = 1000.0                              # used when column is missing
DEFAULT_TAX_RATE = 18

# ---- report explanation rules (descriptive tags only; the NN does the scoring) ----
ITC_RATIO_ALERT = 1.3
REPEAT_PAIR_MIN = 3
NEW_SELLER_DAYS = 180
NEW_SELLER_VOLUME = 1_000_000
FEW_BUYERS_MAX = 3
FEW_BUYERS_VOLUME = 2_000_000
MAX_RING_LENGTH = 6
RING_SCAN_LIMIT = 3000

# ---- overall verdict cut-offs (flag rate %) ----
VERDICT_CRITICAL, VERDICT_HIGH, VERDICT_MODERATE = 10, 5, 1

# ---- training --------------------------------------------------------------
SEED = _int("GST_SEED", 42)
EPOCHS = _int("GST_EPOCHS", 80)
BATCH_SIZE = _int("GST_BATCH_SIZE", 128)
