import subprocess
from pathlib import Path

from template_python.setting import args


def main():
    current_directory = Path(__file__).parent
    module_example_path = current_directory / "module_example.py"

    if args.debug:
        # デバッグ時の設定
        subprocess.run(["python", "-Xfrozen_modules=off", module_example_path], check=True)
    else:
        # 本番環境の設定
        subprocess.run(["python", module_example_path], check=True)

    print(current_directory)


if __name__ == "__main__":
    main()
