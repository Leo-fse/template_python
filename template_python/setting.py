import argparse
from configparser import ConfigParser
from pathlib import Path

parser = argparse.ArgumentParser(description="Run the module example script.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()
debug = args.debug

BASE_DIR = Path(__file__).parent.parent
OUTER_MODULE_DIR = BASE_DIR / "libs"
CONFIG_DIR = BASE_DIR / "config"
LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

#  フォルダが存在しない場合は作成する
for directory in [OUTER_MODULE_DIR, CONFIG_DIR, LOG_DIR, DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


config = ConfigParser()
config.read(CONFIG_DIR / "database.ini")
