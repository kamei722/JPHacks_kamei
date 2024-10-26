from flask import Flask, request, jsonify
from openai import OpenAI
import json
import os

app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def text_to_json(text: str) -> dict:
    """
    テキストを受け取り、OpenAI GPT-4を使用してJSON形式に変換する関数。
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt ="""
    You are an expert in accurately converting input Japanese text to JSON format. Please convert according to the following constraints:
    Output specifications:
    1. output must be in the following JSON format.
    {
    “name": Must be a string consisting of common nouns only. Do not include particles, and classify detailed descriptions in additional_info.
    “quantity": Numerical value only
    “expiration date": The expiration date of the product, inferred from the general one. It should be a specific number of days and the unit should be days.
    “category": Select one of the following categories:. 
                '日用品', '食品', '飲料', 'Other',.
    “additional_info": additional information in string. If none, empty string.
    }

    Strict rules:
    - Do not add any extra description.
    - Always use a format that can be parsed as valid JSON.
    - Japanese strings are output as-is without escaping using UTF-8.
    - Japanese strings are output as-is in UTF-8 without escaping. quantity must be numeric (not a string).
    - Use null or empty string for information that cannot be guessed.

    Example:
    Input: 北海道産の人参を5本買いました.
    Output: {
    “name": ‘人参’,
    “quantity": 5
    “expiry_date": 14 
    “category": ‘食品’,
    “additional_info": ”北海道産”
    }
"""

#     system_prompt = """
# あなたは入力されたテキストを正確にJSON形式に変換する専門家です。以下の制約に従って変換してください：

# 出力仕様:
# 1. 必ず以下のJSON形式で出力すること
# {
#   "name": 一般名詞のみで構成される文字列とする,
#   "quantity": 数値のみ,
#   "expiration date": その商品の賞味期限、消費期限を一般的なものから推測して書く。
#   "category": 以下のカテゴリーのいずれかを選択: 
#               '日用品', '食品', '飲料', '衣類', 'その他',
#   "additional_info": "追加情報を文字列で。ない場合は空文字列"
# }

# 2. 厳格な規則：
# - 余計な説明は一切付けない
# - 必ず有効なJSONとして解析可能な形式にする
# - 日本語の文字列はUTF-8でエスケープせずそのまま出力
# - quantity は必ず数値型（文字列にしない）
# - 推測できない情報は null か 空文字列 を使用
# """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            max_tokens=150,
            temperature=0.2,
        )
        json_response = response.choices[0].message.content
        return json.loads(json_response)

    except Exception as e:
        print(f"Error converting text to JSON: {e}")
        return {}

@app.route('/convert', methods=['POST'])
def convert():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    result = text_to_json(text)
    
    if not result:
        return jsonify({"error": "Conversion failed"}), 500
        
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)