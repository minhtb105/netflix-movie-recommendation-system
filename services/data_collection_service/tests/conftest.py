import sys
from pathlib import Path


service_root = Path(__file__).resolve().parent.parent

if str(service_root) not in sys.path:
    sys.path.insert(0, str(service_root))
