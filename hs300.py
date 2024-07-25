import akshare as ak
import pandas as pd
import numpy as np

# 获取沪深300指数历史数据
stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol="sh000300")

# 将日期列转换为datetime格式
stock_zh_index_daily_df['date'] = pd.to_datetime(stock_zh_index_daily_df['date'])

# 设置日期列为索引
stock_zh_index_daily_df.set_index('date', inplace=True)

#print(stock_zh_index_daily_df)

# 计算每年的涨幅
annual_return = stock_zh_index_daily_df['close'].resample('Y').ffill().pct_change()


# 将年度涨幅结果格式化为百分比
annual_return = annual_return * 100
print(annual_return)
print(','.join(['{:.2f}'.format(x/100+1) for x in annual_return]))

# 将年度涨幅结果限制在-5到25之间
clipped_annual_return = np.clip(annual_return, -5, 25)
print(clipped_annual_return)
print(','.join(['{:.2f}'.format(x/100+1) for x in clipped_annual_return]))
