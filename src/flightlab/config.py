import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")

# Dados pertencem à aplicação, não ao diretório de instalação do pacote.
ROOT = Path(os.environ.get("FLIGHTLAB_HOME", Path.cwd())).resolve()
DATA_PATH = ROOT / "data" / "raw" / "nycflights.csv"
ARTIFACTS = ROOT / "artifacts"
DATA_URL = "https://raw.githubusercontent.com/JackyP/testing/master/datasets/nycflights.csv"
TARGET_MINUTES = 15
CATEGORICAL = ["carrier", "origin", "dest"]
NUMERIC = ["month", "day_of_week", "distance"]
FEATURES = CATEGORICAL + NUMERIC
