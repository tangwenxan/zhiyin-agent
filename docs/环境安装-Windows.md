# Windows 环境安装与常见报错

> 遇到环境问题的第一件事：**关掉终端重开一次**。90% 的"命令找不到"都是装了东西但当前终端还没刷新 PATH。

---

## 一、安装 uv（推荐）

`uv` 是一个独立的可执行程序，用来管理 Python 版本和依赖，比 pip 快很多，而且它会**自动在项目里建一个独立的 `.venv`**，不会污染你的 Anaconda 环境。

### 方式 A · 官方安装脚本（推荐，不依赖 conda）

在 PowerShell 里执行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

装完**关闭终端、重新打开**，然后验证：

```powershell
uv --version
```

### 方式 B · 用你已有的 Anaconda pip（一条命令，最快）

你的终端提示符是 `(base)`，说明 Anaconda 已激活，直接用它的 pip 安装即可：

```powershell
pip install uv
```

装完同样**重开终端**，再 `uv --version`。

### 方式 C · winget

```powershell
winget install --id=astral-sh.uv -e
```

---

## 二、装好之后：跑起来

```powershell
cd D:\agent_project\zhiyin-agent

# 创建隔离环境并安装依赖（首次会下载，耐心等）
uv sync

# 复制配置模板，填你自己的模型 Key
copy .env.example .env

# 冒烟测试：看到模型回话 = 环境通了
uv run python -m zhiyin.llm
```

**关于 `uv run`**：uv 会自动使用项目里的 `.venv`，你**不需要手动激活环境**，每条命令前面加 `uv run` 就行。

---

## 三、备选方案：不用 uv，用 Python 自带的 venv + pip

如果 uv 死活装不上，这条路也能走通，只是后面命令要改成激活环境的方式。

```powershell
cd D:\agent_project\zhiyin-agent

# 1. 建虚拟环境
python -m venv .venv

# 2. 激活
.\.venv\Scripts\Activate.ps1
```

**如果激活时报"禁止运行脚本"**（PowerShell 执行策略限制），先执行一次：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

然后继续：

```powershell
# 3. 升级 pip 并安装项目依赖
python -m pip install -U pip
pip install -e .

# 4. 冒烟测试
python -m zhiyin.llm
```

> 注意：用 venv 方案时，命令里**不要**再加 `uv run`，环境激活后直接用 `python` 即可。
> 每次新开终端都要重新执行一次 `.\.venv\Scripts\Activate.ps1`。

---

## 四、常见报错对照表

| 报错 | 原因 | 解决 |
|---|---|---|
| `无法将"uv"项识别为...` | uv 没装，或装了没重开终端 | 装 uv；然后关掉终端重开 |
| `No solution found when resolving dependencies` | 某个可选依赖包名写错或版本冲突 | 见 `docs/依赖安装清单.md` 的排错速查；本项目已改为按需安装，避免此问题 |
| `无法加载文件 Activate.ps1，因为在此系统上禁止运行脚本` | PowerShell 执行策略限制 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `python 不是内部或外部命令` | Python 没加进 PATH | 重装 Python 时勾选 "Add python.exe to PATH" |
| `No module named zhiyin` | 没安装项目本身 | 在项目根目录执行 `uv sync` 或 `pip install -e .` |
| `缺少 LLM_API_KEY` | `.env` 没建或没填 | `copy .env.example .env` 并填入真实 Key |
| `uv sync` 卡在下载 | 网络慢 | 国内可设镜像：`$env:UV_DEFAULT_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"` |
| 装完跑 `uv sync` 报 Python 版本不符 | 缺 3.11+ | uv 会自动下载所需版本，稍等即可；或 `uv python install 3.11` |

---

## 五、确认清单（全部通过就可以开始 S0 了）

- [ ] `uv --version` 能输出版本号（或 venv 方案下 `python -m zhiyin.llm` 能用）
- [ ] `uv sync` 成功，项目下出现了 `.venv` 文件夹
- [ ] `.env` 已创建并填好 `LLM_API_KEY`
- [ ] `uv run python -m zhiyin.llm` 能看到模型回话
- [ ] `git status` 里**没有** `.env`（确保密钥没被提交）

全部打勾 → 回到《S0-执行指南》，开始 Day 1。
