import akshare as ak
import pandas as pd

# ========== 配置 ==========
stocks = [
    ("sz", "300033"),  # 深市
    ("sh", "600519"),  # 沪市
    ("hk", "00700"),   # 港股
]

alert_days = 5          # 连续多少天作为触发条件
alert_threshold = 0.0   # 阈值（大于此值算流入，小于此值算流出）
output_excel = "stock_fund_flow_monitor.xlsx"

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
        # 资金流向
        df_money = ak.stock_individual_fund_flow(stock=symbol)
        df_money["日期"] = pd.to_datetime(df_money["日期"])
        df_money.set_index("日期", inplace=True)

        # 主力资金占比字段兼容
        if "大单净流入占比" in df_money.columns:
            df_money["主力资金占比"] = df_money["大单净流入占比"]
        elif "主力净流入占比" in df_money.columns:
            df_money["主力资金占比"] = df_money["主力净流入占比"]
        else:
            df_money["主力资金占比"] = df_money.iloc[:, -1]

        df_trend = df_money.tail(20)

        # 筹码分布
        df_chip = ak.stock_chip_distribution_transverse_df(symbol=symbol)

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
        df_chip.to_excel(writer, sheet_name=f"{symbol}_筹码分布")

    except Exception as e:
        print(f"⚠️ {symbol} 数据获取失败：{e}")

# 总览表
df_summary = pd.DataFrame(summary_list)
df_summary.to_excel(writer, sheet_name="汇总", index=False)

writer.close()
print(f"\n✅ 分析完成，结果已保存到 {output_excel}")
