"""依管徑分組統計管線總長度與數量。

輸入：取水管線資料詳細表1080125(test).xlsx / 工作表「管線資料詳細表」
輸出：管徑統計.xlsx
"""
import re

import pandas as pd

SRC = "取水管線資料詳細表1080125(test).xlsx"
DST = "管徑統計.xlsx"

raw = pd.read_excel(SRC, sheet_name="管線資料詳細表", header=None)
print(raw.to_string())  # 列出全部原始資料以便檢查

# 前 3 列為標題；欄 0=管線編號、5=尺寸(mm)、6=管長(m)
data = raw.iloc[3:, [0, 5, 6]].copy()
data.columns = ["管線編號", "尺寸", "管長(m)"]
data["管徑(mm)"] = data["尺寸"].astype(str).str.extract(r"(\d+(?:\.\d+)?)")[0].astype(float)
data["管長(m)"] = pd.to_numeric(data["管長(m)"], errors="coerce")

skipped = data[data["管徑(mm)"].isna() | data["管長(m)"].isna()]
data = data.dropna(subset=["管徑(mm)", "管長(m)"])

summary = (
    data.groupby("管徑(mm)")
    .agg(數量=("管線編號", "count"), **{"總長度(m)": ("管長(m)", "sum")})
    .reset_index()
    .sort_values("管徑(mm)")
)
summary["管徑(mm)"] = summary["管徑(mm)"].map(lambda d: int(d) if d.is_integer() else d)
summary["總長度(m)"] = summary["總長度(m)"].round(2)
total = pd.DataFrame([{"管徑(mm)": "合計", "數量": summary["數量"].sum(),
                       "總長度(m)": round(summary["總長度(m)"].sum(), 2)}])
summary = pd.concat([summary, total], ignore_index=True)

with pd.ExcelWriter(DST, engine="openpyxl") as w:
    summary.to_excel(w, sheet_name="管徑統計", index=False)
    data.drop(columns="尺寸").to_excel(w, sheet_name="明細", index=False)

print("\n略過的列：\n", skipped.to_string() if len(skipped) else "無")
print("\n統計結果：\n", summary.to_string(index=False))
