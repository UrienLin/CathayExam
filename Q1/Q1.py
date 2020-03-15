# coding=UTF-8
import pandas as pd

def load_file():
    path='./'
    df_a = pd.read_csv(path + 'a_lvr_land_a.csv')[1:]
    df_b = pd.read_csv(path + 'b_lvr_land_a.csv')[1:]
    df_e = pd.read_csv(path + 'e_lvr_land_a.csv')[1:]
    df_f = pd.read_csv(path + 'f_lvr_land_a.csv')[1:]
    df_h = pd.read_csv(path + 'h_lvr_land_a.csv')[1:]
    list_df = [df_a, df_b, df_e, df_f, df_h]
    df_all = pd.concat(list_df).reset_index(drop=True)
    return df_all
def filter_a(df_all):
    df_all['總樓層數'] = df_all['總樓層數'].fillna(0)
    filter_pos = (df_all['總樓層數'].str.contains('十',na=False))
    filter_neg = (df_all['總樓層數'].str.contains('^十$|^十一|^十二',na=False))
    filter_a = (df_all['主要用途'] == '住家用') & \
               (df_all['建物型態'].str.contains('住宅大樓'))&\
               (filter_pos) & (~filter_neg)

    df_all[filter_a].to_csv('filter_a_0315.csv', encoding='utf-8', index=False)


def filter_b(df_all):

    def split_park(str_input):
        sub_str_list = str_input.split('土地')[1].split('建物')
        land = int(sub_str_list[0])
        buildings = int(sub_str_list[1].split('車位')[0])
        park = int(sub_str_list[1].split('車位')[1])
        return [land,buildings,park]


    df_all['LBP'] = df_all['交易筆棟數'].apply(split_park)
    _df = pd.DataFrame(list(df_all.LBP))
    _df.columns = ['土地', '建物', '車位']
    df_all = df_all.join(_df)
    df_all['總價元'] = df_all['總價元'].astype(int) 
    df_all['車位總價元'] = df_all['車位總價元'].astype(int)
    df_all['車位移轉總面積平方公尺'] = df_all['車位移轉總面積平方公尺'].astype(float)
    
    #條件 僅計算有車位總價 有車位移轉總面積平方公尺 且交易筆棟數車位不為0 的項目
    filter_park = (df_all['車位總價元'] != 0) & (df_all['車位移轉總面積平方公尺']!=0) & (df_all['車位']!=0)
    filter_cols = ['車位類別','車位移轉總面積平方公尺','車位','車位總價元','車位均價元']
    #將車位總價 除以 車位數 作為 車位均價元
    df_all['車位均價元'] =df_all['車位總價元'] / df_all['車位'] 

    trade = df_all['交易標的'].count()
    park = df_all['車位'].sum()
    avg_price = df_all['總價元'].mean()
    avg_park_price = df_all[df_all['車位均價元'] != 0 ]['車位均價元'].mean()

    ans = pd.DataFrame([[trade, park, round(avg_price), round(avg_park_price)]])
    ans.columns=['總件數', '總車位數', '平均總價元', '平均車位總價元']
    ans.to_csv('filter_b_0315.csv', encoding='utf-8', index=False)

if __name__ == '__main__':
    df = load_file()
    filter_a(df)
    filter_b(df)
