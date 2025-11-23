import akshare

import akshare as ak

print("版本:", akshare.__version__)
print("是否有新接口：", hasattr(akshare, "stock_individual_fund_flow_stock"))
print("是否有港股接口：", hasattr(akshare, "stock_hk_fund_flow_rank_em"))

print(akshare.__file__)

try:
    data = ak.stock_hk_spot_em()
    print("✅ 港股接口可用")
except AttributeError:
    print("❌ 当前 AkShare 版本未提供港股接口")
