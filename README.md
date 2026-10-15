# TankBattle

这是 TankBattle（坦克大战）的仓库，包含你的游戏源码与资源。

快速运行（在本地）：
1. 克隆仓库并进入目录：
   git clone git@github.com:Kekexi-ode/TankBattle.git
   cd TankBattle

2. 推荐创建并激活虚拟环境：
   python -m venv .venv
   # macOS / Linux
   source .venv/bin/activate
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

3. 安装依赖：
   python -m pip install --upgrade pip
   pip install pygame

4. 运行游戏（两种方式任选其一）：
   # 直接运行你上传的脚本：
   python "坦克大战/main.py"

   # 或者用模块入口（推荐）：
   python -m tankbattle

说明：为了避免改动你现有的文件，我添加了一个包装模块（`tankbattle`），它会在运行时调用你上传的 `坦克大战/main.py`。

如果你愿意，我也可以把代码整理为标准的包结构（把源码移到 `src/tankbattle/` 并把资源放到 `tankbattle/images/`），这样更利于发布与安装；这一步会修改很多文件，提交前我会先把将要移动的文件列表发给你确认。

如果运行时遇到错误，请把终端的报错信息粘贴给我，我会帮你排查。