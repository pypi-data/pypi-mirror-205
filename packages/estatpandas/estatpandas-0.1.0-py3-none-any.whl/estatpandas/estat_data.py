import requests
import json
import pandas as pd

def download_estat_data(api_key, stats_data_id, start_position, max_records):
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
    url = f"{base_url}?appId={api_key}&statsDataId={stats_data_id}&startPosition={start_position}&limit={max_records}"
    response = requests.get(url)

    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON at start_position: {start_position}")
        return None

    if data['GET_STATS_DATA']['RESULT']['STATUS'] == "ERROR":
        raise ValueError(f"Error: {data['GET_STATS_DATA']['RESULT']['ERROR_MSG']}")

    data_table = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']
    df = pd.DataFrame(data_table)
    return df

def get_metadata(api_key, stats_data_id):
    base_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo"
    url = f"{base_url}?appId={api_key}&statsDataId={stats_data_id}"
    response = requests.get(url)
    data = response.json()

    if data['GET_META_INFO']['RESULT']['STATUS'] == "ERROR":
        raise ValueError(f"Error: {data['GET_META_INFO']['RESULT']['ERROR_MSG']}")

    return data['GET_META_INFO']['METADATA_INF']

def get_estat_dataframe(api_key, stats_data_id):
    start_position = 1
    max_records = 100000
    all_data = pd.DataFrame()

    while True:
        df = download_estat_data(api_key, stats_data_id, start_position, max_records)

        if df is not None:
            all_data = pd.concat([all_data, df], ignore_index=True)

        if df is None or len(df) < max_records:
            break
        else:
            start_position += max_records

    metadata = get_metadata(api_key, stats_data_id)
    class_objects = metadata['CLASS_INF']['CLASS_OBJ']

    data = []
    for class_obj in class_objects:
        column_id = class_obj["@id"]
        column_name = class_obj["@name"]
        for class_item in class_obj["CLASS"]:
            code = class_item["@code"]
            name = class_item["@name"]
            level = class_item["@level"]
            parent_code = class_item.get("@parentCode", "")
            data.append([column_id, column_name, code, name, level, parent_code])

    columns = ["id", "name", "code", "class_name", "level", "parent_code"]
    df = pd.DataFrame(data, columns=columns)

    column_mapping = {}
    for _, row in df.iterrows():
        column_id = row["id"]
        code = row["code"]
        class_name = row["class_name"]
        if column_id not in column_mapping:
            column_mapping[column_id] = {}
        column_mapping[column_id][code] = class_name

    for column_id, code_map in column_mapping.items():
        column_name = f"@{column_id}"
        all_data[column_name] = all_data[column_name].map(code_map)

    column_name_mapping = df.set_index("id")["name"].to_dict()
    column_name_mapping = {f"@{k}": v for k, v in column_name_mapping.items()}
    all_data = all_data.rename(columns=column_name_mapping)
    all_data = all_data.rename(columns={"@unit" : "単位", "$":"値"})
    estat_df = all_data.copy()
    
    return estat_df



