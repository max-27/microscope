from pathlib import Path
import os

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_PATH = os.path.join(ROOT_PATH.parent, "data", "simulation")