import argparse
import os
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Run the module example script.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    current_directory = Path(__file__).parent
    module_example_path = current_directory / "module_example.py"

    if args.debug:
        # デバッグ時の設定
        os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
        subprocess.run(["python", "-Xfrozen_modules=off", module_example_path], check=True)
    else:
        # 本番環境の設定
        subprocess.run(["python", module_example_path], check=True)

    print(current_directory)


if __name__ == "__main__":
    main()
