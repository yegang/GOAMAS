import akshare as ak

# 先测试 A 股
try:
    df = ak.stock_individual_fund_flow(stock="300033")  # 不加 sz
    print(df.head())
except Exception as e:
    print("失败1:", e)

try:
    df = ak.stock_individual_fund_flow(stock="sz300033")  # 加 sz
    print(df.head())
except Exception as e:
    print("失败2:", e)

# 再测试 沪市
try:
    df = ak.stock_individual_fund_flow(stock="600519")
    print(df.head())
except Exception as e:
    print("失败3:", e)

try:
    df = ak.stock_individual_fund_flow(stock="sh600519")
    print(df.head())
except Exception as e:
    print("失败4:", e)

# 港股可能需要用另一个接口
try:
    df = ak.stock_hk_fund_flow_rank_em(symbol="00700")
    print(df.head())
except Exception as e:
    print("港股失败:", e)
