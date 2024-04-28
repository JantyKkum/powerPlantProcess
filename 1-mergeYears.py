"""
# @Software: PyCharm
# @File: 1-mergeYears.py
# @Author: YiTao Jian
# @Institution: Shanghai Jiao Tong University, Shanghai, China
# @E-mail: jianyitao@sjtu.edu.cn
# @Site: 
# @Time: 2024/4/28 16:38
# @Description:
【Step1】：合并各个省份的年份数据，测试数据以北京为例
【逻辑】：仅仅合并名字一样的电厂，否则单独成行
"""
import pandas as pd

province = '北京'
years = range(2003, 2022) #缺少13,16,20数据

# 创建一个空的DataFrame用于存储合并后的数据
merged_data = pd.DataFrame()

for year in years:
    # 排除2013及2016年份
    if year in [2013, 2016, 2020]:
        continue

    # 读取每个年份的数据
    # 尝试使用不同的编码格式进行读取
    try:
        data = pd.read_excel(f"./rawData/cec/{province}/{year}{province}.xlsx")
    except UnicodeDecodeError:
        data = pd.read_excel(f"./rawData/cec/{province}/{year}{province}.xlsx", encoding='gbk')
        print("使用gbk编码格式读取数据")

    # 在合并前重命名列，以避免列名冲突
    data = data.rename(columns={
        'Plant Capacity(KW)': f'{year}_Capacity(KW)',
        'Generation (MWh）': f'{year}_Generation(MWh)',
        '供电标准煤耗率(克/千瓦时)': f'{year}_供电标准煤耗率(克/千瓦时)',
        '发电标准煤耗率(克/千瓦时)': f'{year}_发电标准煤耗率(克/千瓦时)',
        '发电厂用电率(%)': f'{year}_发电厂用电率(%)',
        '发电设备平均利用小时(小时)': f'{year}_发电设备平均利用小时(小时)',
        '发电耗用原煤量(吨)': f'{year}_发电耗用原煤量(吨)',
        '发电耗用燃油量(吨)': f'{year}_发电耗用燃油量(吨)',
        '发电耗用燃气量(万立方米)': f'{year}_发电耗用燃气量(万立方米)'
    })

    # 合并数据
    if merged_data.empty:
        merged_data = data
    else:
        merged_data = pd.merge(merged_data, data, on='company_name', how='outer')


# 如果需要保存合并后的数据
merged_data.to_csv(f"{province}_merged_years.csv", index=False)

