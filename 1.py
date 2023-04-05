# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json

# AnkiConnect 的 API 端点
anki_endpoint = "http://localhost:8765"

# 查询条件
query = "deck:読みちゃん"

# AnkiConnect 查询笔记的 API
find_notes_api = anki_endpoint + "/query"

# AnkiConnect API 参数
params = {
    "action": "findNotes",
    "version": 6,
    "params": {
        "query": query
    }
}

# 发送请求
response = requests.post(anki_endpoint, json=params)

# 获取查询结果
result = response.json()

if result["error"] is not None:
    print("AnkiConnect API error:", result["error"])
else:
    print("Note ids:", result["result"][0])

# 获取field value

card_id = result["result"][0]

headers = {"Content-Type": "application/json"}
payload = {"action": "notesInfo", "version": 6, "params": {"notes": [card_id]}}

# 发送请求并获取响应
response = requests.post(anki_endpoint, headers=headers, data=json.dumps(payload))

field_value = response.json()['result'][0]['fields']['日文']['value']

print(field_value)











url = 'https://dict.asia/jc/' + field_value

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
results = soup.find_all('div', {'id': 'jp_com_panel_0'})

expression = ""
for result in results:
    for text in result.find('span', {'class': 'commentItem'}).stripped_strings:
            expression += text + '\n'
    break




print(expression)



# 修改field值

data = {
    "action": "updateNoteFields",
    "version": 6,
    "params": {
        "note": {
            "id": card_id,  # 要修改的卡片 ID
            "fields": {
                "释意": expression,  # 要修改的字段名及内容
            }
        }
    }
}

response = requests.post(anki_endpoint, headers=headers, data=json.dumps(data))
# 输出响应结果
print(response.json())




