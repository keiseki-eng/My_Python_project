import os
import sys
import yaml

# config.yaml のパスを指定して読み込み
conf_path = os.path.join( '../config/config.yaml')
with open(conf_path, 'r') as f:
    config = yaml.safe_load(f)



def extract_unique_tags(df, column_name):
    unique_tags = set()
    # カラムが存在すること、かつ完全に null ではないことを確認
    if column_name in df.columns and not df[column_name].isnull().all():
        # split 時のエラー回避のため、NaN を空文字に置換
        df_temp = df[column_name].fillna('')
        for entry in df_temp:
            if entry:
                tags = entry.split('/')
                unique_tags.update(tags)
    return sorted(list(unique_tags))


def create_tag_features(df, unique_tags):
    new_tag_features_local = []
    for tag in unique_tags:
        col_name = f'tag_{tag}'
        # 新しい二値カラムを作成。'statuses' が NaN の場合は fillna('') でエラー回避
        df[col_name] = df['statuses'].fillna('').apply(lambda x: 1 if tag in x.split('/') else 0)
        new_tag_features_local.append(col_name)
    return df, new_tag_features_local
