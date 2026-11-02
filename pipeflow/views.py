import math

from django.shortcuts import render


def manning_full_pipe(diameter_mm, slope_percent, n):
    """圓管滿流：曼寧公式。回傳 (流速 m/s, 流量 m³/s)。"""
    d = diameter_mm / 1000.0          # m
    s = slope_percent / 100.0         # m/m
    area = math.pi * d ** 2 / 4       # 通水斷面積 A
    r = d / 4                         # 水力半徑 R = D/4（滿流）
    v = (1.0 / n) * r ** (2.0 / 3.0) * math.sqrt(s)
    q = v * area
    return v, q


def index(request):
    ctx = {"diameter": "", "slope": "", "n": "0.013"}
    if request.method == "POST":
        ctx.update(
            diameter=request.POST.get("diameter", ""),
            slope=request.POST.get("slope", ""),
            n=request.POST.get("n", ""),
        )
        try:
            d = float(ctx["diameter"])
            s = float(ctx["slope"])
            n = float(ctx["n"])
            if d <= 0 or s <= 0 or n <= 0:
                raise ValueError
            v, q = manning_full_pipe(d, s, n)
            ctx["velocity"] = f"{v:.3f}"
            ctx["flow"] = f"{q:.4f}"
        except ValueError:
            ctx["error"] = "請輸入大於 0 的數值。"
    return render(request, "pipeflow/index.html", ctx)
