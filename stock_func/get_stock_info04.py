import akshare as ak
import pandas as pd

# ========== 配置 ==========
stocks = [
    ("sz", "300033"),  # 深市
    ("sh", "600519"),  # 沪市
    ("hk", "00700"),   # 港股
]

alert_days = 5
alert_threshold = 0.0
output_excel = "stock_fund_flow_monitor.xlsx"

def check_alerts(df, col="主力资金占比", days=5, threshold=0.0):
    alerts = []
    if len(df) >= days:
        recent = df[col].tail(days)
        if all(recent > threshold):
            alerts.append(f"最近{days}天主力资金占比均 > {threshold}，可能有主力吸筹")
        elif all(recent < threshold):
            alerts.append(f"最近{days}天主力资金占比均 < {threshold}，可能有主力出货")
    return alerts

summary_list = []
writer = pd.ExcelWriter(output_excel, engine="openpyxl")

for market_code, stock_code in stocks:
    symbol = market_code + stock_code
    print(f"\n=== 分析 {symbol} ===")
    try:
        # ========== 根据市场选择接口 ==========
        if market_code in ["sh", "sz"]:
            df_money = ak.stock_individual_fund_flow_stock(symbol=stock_code)
        elif market_code == "hk":
            df_money = ak.stock_hk_fund_flow_rank_em()
            df_money = df_money[df_money["股票代码"] == stock_code]

        if df_money is None or df_money.empty:
            raise ValueError("资金流向数据为空")

        # 日期处理
        if "日期" in df_money.columns:
            df_money["日期"] = pd.to_datetime(df_money["日期"])
            df_money.set_index("日期", inplace=True)

        # 主力资金占比字段
        for col_candidate in ["主力净流入占比", "大单净流入占比", "净大单占比"]:
            if col_candidate in df_money.columns:
                df_money["主力资金占比"] = df_money[col_candidate]
                break
        else:
            df_money["主力资金占比"] = df_money.iloc[:, -1]

        df_trend = df_money.tail(20)

        # 筹码分布（仅 A 股可用）
        df_chip = None
        if market_code in ["sh", "sz"]:
            try:
                df_chip = ak.stock_chip_distribution_transverse_df(symbol=symbol)
            except:
                df_chip = pd.DataFrame()

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
        if df_chip is not None and not df_chip.empty:
            df_chip.to_excel(writer, sheet_name=f"{symbol}_筹码分布")

    except Exception as e:
        print(f"⚠️ {symbol} 数据获取失败：{e}")

# 汇总
df_summary = pd.DataFrame(summary_list)
df_summary.to_excel(writer, sheet_name="汇总", index=False)
writer.close()

print(f"\n✅ 分析完成，结果已保存到 {output_excel}")
