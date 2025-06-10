# start-gaijin.py (已为 GitHub Actions 修改的版本)
import json
import requests
import time
import datetime
import pytz
import csv
import traceback

def fetch_and_append_data():
    url = "https://www.chinamoney.com.cn/r/cms/www/chinamoney/data/fx/rfx-sp-quot.json"
    # 使用相对路径，数据文件将保存在仓库根目录
    output_file = "data3.csv" 

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        beijing_tz = pytz.timezone('Asia/Shanghai')
        current_time = datetime.datetime.now(beijing_tz).strftime('%Y-%m-%d %H:%M:%S')

        items = data.get('records', [])
        if not items:
            print(f"No data found in JSON from {url}")
            return

        file_exists = False
        try:
            with open(output_file, 'r') as f:
                if f.readline(): # 检查文件是否为空
                    file_exists = True
        except FileNotFoundError:
            file_exists = False
            
        with open(output_file, 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            # 只有当文件是新创建的时，才写入表头
            if not file_exists and items:
                headers = list(items[0].keys()) + ['timestamp']
                writer.writerow(headers)
            
            # 直接从第一个 item 获取表头结构来处理所有行
            headers_for_rows = list(items[0].keys()) + ['timestamp']
            for item in items:
                if isinstance(item, dict):
                    row = [item.get(header, '') for header in headers_for_rows[:-1]]
                    row.append(current_time)
                    writer.writerow(row)
                else:
                    print(f"Skipping item with unexpected structure: {item}")

        print(f"Data fetched and appended to {output_file} at {current_time}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {url}. Response text: {response.text[:200]}") # 打印部分响应内容以帮助调试
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

# 主执行入口：直接调用函数一次
if __name__ == "__main__":
    fetch_and_append_data()