import pandas as pd
import numpy as np

# 模拟数据
data = {
    'date': pd.date_range(start='2020-12-28', end='2021-01-05'),
    'close': [4000, np.nan, np.nan, np.nan, 4350, 4400, 4800, 4900, 4950]
}

df = pd.DataFrame(data)

# 将日期列设置为索引
df.set_index('date', inplace=True)

# 使用fillna和ffill填充缺失值
df_filled = df.fillna(method='ffill')

# 显示原始数据
print("原始数据:")
print(df)

# 按年重采样并进行前向填充
df_resampled = df_filled.resample('Y').ffill()

# 显示重采样并前向填充之后的数据
print("\n重采样并前向填充之后的数据:")
print(df_resampled)

# 计算年内涨幅百分比
annual_return = df_resampled['close'].pct_change() * 100

print("\n年度涨幅:")
print(annual_return)
