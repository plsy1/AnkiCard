# -*- coding: utf-8 -*-

import json
import requests
from bs4 import BeautifulSoup
import time


# 查询 Anki 笔记
def find_notes(query):
    # AnkiConnect 的 API 端点
    anki_endpoint = "http://localhost:8765"

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
        return result["result"]


# 获取笔记的字段值
def get_field_value(card_id):
    # AnkiConnect 的 API 端点
    anki_endpoint = "http://localhost:8765"

    headers = {"Content-Type": "application/json"}
    payload = {"action": "notesInfo", "version": 6, "params": {"notes": [card_id]}}

    # 发送请求并获取响应
    response = requests.post(anki_endpoint, headers=headers, data=json.dumps(payload))

    # 获取字段值
    field_value = response.json()['result'][0]['fields']['日文']['value']
    return field_value


# 查询释义
def query_expression(field_value):
    url = 'https://dict.asia/jc/' + field_value

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', {'id': 'jp_com_panel_0'})

    expression = ""
    for result in results:
        for text in result.find('span', {'class': 'commentItem'}).stripped_strings:
                expression += text + "<br>"
                # anki中使用css渲染，换行用<br>
        break
    return expression


# 修改笔记字段值
def update_note_fields(card_id, expression):
    # AnkiConnect 的 API 端点
    anki_endpoint = "http://localhost:8765"

    # AnkiConnect API 参数
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

    headers = {"Content-Type": "application/json"}

    response = requests.post(anki_endpoint, headers=headers, data=json.dumps(data, indent=2))
    # 输出响应结果
    print(response.json())


if __name__ == '__main__':
    query = "deck:読みちゃん"
    note_ids = find_notes(query)
    # print(note_ids)

    cardNumber = None

    with open("len.txt",'r') as f:
        content = f.read() 
        cardNumber = int(content)
        
    print("将从 " + str(cardNumber) + " 处开始添加。\n")

    for id in note_ids[cardNumber:]:
        field_value = get_field_value(id)
        print(field_value)
        expression = query_expression(field_value)
        print(expression)
        update_note_fields(id, expression)
        time.sleep(2)
    
    cardNumber = len(note_ids)
    with open("len.txt",'w') as f:
        f.write(str(cardNumber))
