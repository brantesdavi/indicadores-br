from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
#assim ele descobre a apsta raiz automaticamente

from db import get_engine



engine = get_engine()