import pandas as pd


def compare_name(name1, name2, threshold=0.8):
    len1 = len(name1)
    len2 = len(name2)
    same_len = 0
    if len1 == len2:
        for i in range(len1):
            if name1[i] == name2[i]:
                same_len += 1
        if same_len / len1 >= threshold:
            return True
        return False
    else:
        raise ValueError("The length of two names are not equal.")


def compare(company_name1, df2, company_name2_col, value1_col, value2_col, value3_col, value4_col, threshold=0.75):
    match_counts = {}
    for i in range(len(company_name1)):
        for j in range(len(df2)):
            if isinstance(company_name1[i], str) and isinstance(df2[company_name2_col][j], str):
                if len(company_name1[i]) == len(df2[company_name2_col][j]):
                    if compare_name(company_name1[i], df2[company_name2_col][j], threshold):
                        match_counts[df2[company_name2_col][j]] = match_counts.get(df2[company_name2_col][j], 0) + 1

    for i in range(len(company_name1)):
        for j in range(len(df2)):
            if isinstance(company_name1[i], str) and isinstance(df2[company_name2_col][j], str):
                if len(company_name1[i]) == len(df2[company_name2_col][j]):
                    if compare_name(company_name1[i], df2[company_name2_col][j], threshold):
                        n = match_counts[df2[company_name2_col][j]]
                        if df2.at[j, value2_col] == 0:
                            df2.at[j, value2_col] = float(value1_col[i]) / (1000 * n)
                        if df2.at[j, value3_col] == 0:
                            df2.at[j, value3_col] = float(value4_col[i]) * 10 / n
    for i, name1 in enumerate(company_name1):
        if name1 not in match_counts:
            new_row = pd.DataFrame([{
                company_name2_col: name1,
                value2_col: value1_col.iloc[i] / 1000,
                value3_col: value4_col.iloc[i] * 10,
            }])
            df2 = pd.concat([df2, new_row], ignore_index=True)
    return df2


def process_data_for_province_and_year(province, years):
    # 这里的基准表文件路径是按我自己习惯建立的，请根据你们自己的文件目录进行调整
    df_base = pd.read_excel(f"data/baseData/{province}/{province}（以2016为基准）.xlsx")
    # 逐年处理电厂数据
    for year in years:
        # 排除2013及2016年份
        if year in [2013, 2016]:
            continue

        print(f'处理{province}省{year}年数据中...')
        # 这里的标准制表文件路径是按我自己习惯建立的，请根据你们自己的文件目录进行调整
        df_processed_data = pd.read_excel(f'data/resourceData/{province}/{year}{province}.xlsx')
        df_processed_data.fillna(0, inplace=True)

        df_base[f'{year} new Plant Capacity(KW)0.75'] = 0
        df_base[f'{year} new Generation (MWh)0.75'] = 0
        df_base[f'{year} new Plant Capacity(KW)1'] = 0
        df_base[f'{year} new Generation (MWh)1'] = 0

        df_base = compare(df_processed_data['company_name'], df_base, '中文名称', df_processed_data['Plant Capacity(KW)'],
                          f'{year} new Plant Capacity(KW)0.75', f'{year} new Generation (MWh)0.75',
                          df_processed_data['Generation (MWh）'])
        df_base = compare(df_processed_data['company_name'], df_base, '中文名称', df_processed_data['Plant Capacity(KW)'],
                          f'{year} new Plant Capacity(KW)1', f'{year} new Generation (MWh)1',
                          df_processed_data['Generation (MWh）'], 1)

    df_base.to_excel(f"data/baseData/{province}/Rystad-{province}.xlsx", index=False)


if __name__ == '__main__':
    # 处理多个省份和多个年份，可以自行添加
    # provinces = ['北京', '湖南', '四川']
    provinces = ['四川']
    # 设置处理的年份范围，可根据实际情况进行调整
    years = range(2001, 2010)

    for province in provinces:
        process_data_for_province_and_year(province, years)