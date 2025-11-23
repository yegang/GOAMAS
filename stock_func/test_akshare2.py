import akshare as ak

print("版本:", ak.__version__)
print(ak.__file__)

# 自动兼容 A 股资金流接口（旧版、新版）
a_share_func = None
for name in [
    "stock_individual_fund_flow_stock",  # 旧接口
    "stock_individual_fund_flow_rank",   # 新接口
]:
    if hasattr(ak, name):
        a_share_func = getattr(ak, name)
        print(f"✅ 找到 A股资金流接口: {name}")
        break

if not a_share_func:
    print("❌ 未找到 A股资金流接口")

# 港股接口检测
try:
    ak.stock_hk_fund_flow_rank_em()
    print("✅ 港股资金流接口可用")
except AttributeError:
    print("❌ 未找到 港股资金流接口")
except Exception as e:
    print("⚠️ 港股接口存在，但调用异常：", e)
