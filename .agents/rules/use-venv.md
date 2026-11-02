# 使用專案 venv 執行 Python

- 在此專案中執行任何 Python 相關指令時，一律使用專案根目錄的虛擬環境 `venv`。
- Python 直譯器：`.\venv\Scripts\python.exe`
- 安裝套件：`.\venv\Scripts\python.exe -m pip install <套件>`
- 執行工具（如 pytest）：`.\venv\Scripts\python.exe -m <模組>`
- 不要使用系統全域的 `python` / `pip`。
