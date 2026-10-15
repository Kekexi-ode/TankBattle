"""
Entrypoint that runs the uploaded game script ("坦克大战/main.py").
This approach avoids renaming/moving your existing files.
"""

import runpy
from pathlib import Path
import sys

def main():
    repo_root = Path(__file__).resolve().parents[2]
    game_script = repo_root / "坦克大战" / "main.py"
    if not game_script.exists():
        print("错误：找不到游戏主程序：{}".format(game_script))
        print("请确认文件位置，或将你的主程序放在 仓库根目录/坦克大战/main.py")
        sys.exit(1)

    # Run the target script as __main__ so it behaves like `python main.py`
    runpy.run_path(str(game_script), run_name="__main__")

if __name__ == "__main__":
    main()
