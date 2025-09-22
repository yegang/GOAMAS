import akshare as ak
import pandas as pd

# ========== 配置 ==========
stocks = [
    ("sz", "300033"),  # 深市
    ("sh", "600519"),  # 沪市
    ("hk", "00700"),   # 港股
]

alert_days = 5          # 连续多少天作为触发条件
alert_threshold = 0.0   # 阈值
output_excel = "stock_fund_flow_monitor.xlsx"


# ========== 数据获取函数 ==========
def get_stock_fund_flow(market_code: str, stock_code: str) -> pd.DataFrame:
    """
    根据市场和股票代码获取资金流数据
    :param market_code: "sz"|"sh"|"hk"
    :param stock_code: 股票代码 (不带 sz/sh/hk 前缀)
    :return: pd.DataFrame，带有 "主力资金占比" 字段
    """
    df_money = None

    if market_code in ["sz", "sh"]:  # A股
        df_money = ak.stock_individual_fund_flow(stock=stock_code)

    elif market_code == "hk":  # 港股（AkShare 没有单股历史资金流，用排行替代）
        df_money = ak.stock_hk_fund_flow_rank_em(symbol="南向资金")
        df_money = df_money[df_money["代码"] == stock_code]

    if df_money is None or df_money.empty:
        return pd.DataFrame()

    # 日期兼容
    if "日期" in df_money.columns:
        df_money["日期"] = pd.to_datetime(df_money["日期"])
        df_money.set_index("日期", inplace=True)

    # 主力资金占比字段兼容
    if "大单净流入占比" in df_money.columns:
        df_money["主力资金占比"] = df_money["大单净流入占比"]
    elif "主力净流入占比" in df_money.columns:
        df_money["主力资金占比"] = df_money["主力净流入占比"]
    else:
        df_money["主力资金占比"] = df_money.iloc[:, -1]

    return df_money


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
        # 获取资金流数据
        df_money = get_stock_fund_flow(market_code, stock_code)
        if df_money.empty:
            raise ValueError("资金流接口无返回")

        df_trend = df_money.tail(20)

        # 筹码分布 (仅 A股支持)
        if market_code in ["sz", "sh"]:
            df_chip = ak.stock_chip_distribution_transverse_df(symbol=stock_code)
            df_chip.to_excel(writer, sheet_name=f"{symbol}_筹码分布")

        # 预警
        alerts = check_alerts(df_trend, days=alert_days, threshold=alert_threshold)
        alert_msg = " | ".join(alerts) if alerts else "无明显预警"

        summary_list.append({
            "股票": symbol,
            "最近主力资金占比": df_trend["主力资金占比"].iloc[-1],
            "预警": alert_msg
        })

        # 写入 Excel
        df_trend.to_excel(writer, sheet_name=f"{symbol}_资金流向")

    except Exception as e:
        print(f"⚠️ {symbol} 数据获取失败：{e}")

# 总览表
df_summary = pd.DataFrame(summary_list)
df_summary.to_excel(writer, sheet_name="汇总", index=False)

writer.close()
print(f"\n✅ 分析完成，结果已保存到 {output_excel}")
