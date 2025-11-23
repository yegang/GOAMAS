import akshare as ak
import pandas as pd

# ========== 配置 ==========
stocks = [
    ("sz", "300033"),
    ("sh", "600519"),
    ("hk", "00700"),
]

alert_days = 5
alert_threshold = 0.0
output_excel = "stock_fund_flow_monitor.xlsx"

# ========== 动态检测接口 ==========
# A股资金流接口
if hasattr(ak, "stock_individual_fund_flow_stock"):
    get_a_fund_flow = ak.stock_individual_fund_flow_stock
elif hasattr(ak, "stock_individual_fund_flow_rank"):
    get_a_fund_flow = ak.stock_individual_fund_flow_rank
else:
    get_a_fund_flow = None

# 港股资金流接口
get_hk_fund_flow = getattr(ak, "stock_hk_fund_flow_rank_em", None)

# ========== 预警函数 ==========
def check_alerts(df, col="主力资金占比", days=5, threshold=0.0):
    alerts = []
    if len(df) >= days:
        recent = df[col].tail(days)
        if all(recent > threshold):
            alerts.append(f"最近{days}天主力资金占比均 > {threshold}，可能有主力吸筹")
        elif all(recent < threshold):
            alerts.append(f"最近{days}天主力资金占比均 < {threshold}，可能有主力出货")
    return alerts

# ========== 主流程 ==========
summary_list = []
writer = pd.ExcelWriter(output_excel, engine="openpyxl")

for market_code, stock_code in stocks:
    symbol = market_code + stock_code
    print(f"\n=== 分析 {symbol} ===")

    try:
        # --- 资金流向 ---
        if market_code in ("sh", "sz"):
            if not get_a_fund_flow:
                raise Exception("当前 AkShare 版本不支持 A股资金流接口")
            df_money = get_a_fund_flow()
            if "股票代码" in df_money.columns:
                df_money = df_money[df_money["股票代码"].str.endswith(stock_code)]
            else:
                raise Exception("接口返回数据不含 股票代码 字段")

        elif market_code == "hk":
            if get_hk_fund_flow:
                df_money = get_hk_fund_flow()
                df_money = df_money[df_money["股票代码"].str.endswith(stock_code)]
            else:
                # 腾讯接口替代
                df_money = ak.stock_hk_spot_em()
                df_money = df_money[df_money["代码"].str.endswith(stock_code)]
                # 构造一个“主力资金占比”列（用成交额占比或成交量占比做近似）
                total_amount = df_money["成交额(港币)"].sum()
                df_money["主力资金占比"] = df_money["成交额(港币)"] / total_amount * 100

        else:
            raise Exception(f"未知市场代码: {market_code}")

        if df_money.empty:
            raise Exception("未获取到资金流数据")

        df_trend = df_money.tail(20)

        # --- 筹码分布 ---
        try:
            df_chip = ak.stock_chip_distribution_transverse_df(symbol=symbol)
        except Exception as e:
            df_chip = pd.DataFrame()
            print(f"⚠️ 筹码数据获取失败：{e}")

        # --- 预警 ---
        alerts = check_alerts(df_trend, days=alert_days, threshold=alert_threshold)
        alert_msg = " | ".join(alerts) if alerts else "无明显预警"

        summary_list.append({
            "股票": symbol,
            "最近主力资金占比": df_trend["主力资金占比"].iloc[-1],
            "预警": alert_msg
        })

        # --- 写入 Excel ---
        df_trend.to_excel(writer, sheet_name=f"{symbol}_资金流向")
        if not df_chip.empty:
            df_chip.to_excel(writer, sheet_name=f"{symbol}_筹码分布")

    except Exception as e:
        print(f"⚠️ {symbol} 数据获取失败：{e}")

# 汇总表
df_summary = pd.DataFrame(summary_list)
df_summary.to_excel(writer, sheet_name="汇总", index=False)

writer.close()
print(f"\n✅ 分析完成，结果已保存到 {output_excel}")
