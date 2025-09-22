import akshare as ak
import pandas as pd

# ========== 配置 ==========
stocks = ["600519", "300033", "00700", "hk00700"]  # 批量股票
output_excel = "fund_flow_batch.xlsx"

# ========== 获取资金流函数 ==========
def get_fund_flow(symbol: str):
    """
    根据股票代码自动获取资金流向数据
    支持：沪深A股（主板）、港股（需升级akshare），创业板暂不支持
    """
    try:
        # -------- A股处理 --------
        if symbol.isdigit() and len(symbol) == 6:
            if symbol.startswith(("6", "0")):   # 主板（上证/深证主板）
                df = ak.stock_individual_fund_flow(stock=symbol)
                if df is not None:
                    return df
                else:
                    return f"⚠️ A股 {symbol} 没有返回数据"
            elif symbol.startswith("3"):  # 创业板
                return f"⚠️ 创业板 {symbol} 暂不支持资金流向"

        # -------- 港股处理 --------
        if symbol.lower().startswith("hk") or (symbol.isdigit() and len(symbol) == 5):
            try:
                # 注意：接口可能随 akshare 版本不同
                df = ak.stock_hk_fund_flow(symbol="南向资金")
                return df
            except Exception:
                return f"⚠️ 港股 {symbol} 接口不支持，请升级 akshare"

        return f"⚠️ 无法识别的代码格式: {symbol}"

    except Exception as e:
        return f"⚠️ {symbol} 获取失败: {e}"


# ========== 批量分析 ==========
writer = pd.ExcelWriter(output_excel, engine="openpyxl")
summary_list = []

for symbol in stocks:
    print(f"\n=== 分析 {symbol} ===")
    df = get_fund_flow(symbol)

    if isinstance(df, str):
        print(df)
        summary_list.append({"股票": symbol, "状态": df})
    else:
        print(df.head())
        sheet_name = f"{symbol}"
        try:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        except:
            # sheet name 太长或特殊字符，截取前 20 个字符
            df.to_excel(writer, sheet_name=sheet_name[:20], index=False)
        summary_list.append({"股票": symbol, "状态": "✅ 成功"})

# 汇总表
df_summary = pd.DataFrame(summary_list)
df_summary.to_excel(writer, sheet_name="汇总", index=False)
writer.close()

print(f"\n✅ 批量分析完成，结果已保存到 {output_excel}")
