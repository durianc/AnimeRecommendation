import csv
from collections import defaultdict

# 用于存储合并后的数据
merged_data = defaultdict(dict)

# 读取第一个 CSV 文件
with open('anime.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        anime_id = row['anime_id']
        merged_data[anime_id].update(row)

# 读取第二个 CSV 文件并合并
with open('output.csv', mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        anime_id = row['anime_id']
        if anime_id in merged_data:
            merged_data[anime_id].update(row)

# 将合并后的数据写入新的 CSV 文件
with open('anime_info.csv', mode='w', encoding='utf-8', newline='') as outfile:
    fieldnames = merged_data[next(iter(merged_data))].keys()
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    for anime_id, data in merged_data.items():
        writer.writerow(data)