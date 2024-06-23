import argparse

parser = argparse.ArgumentParser(description="Run the module example script.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()
