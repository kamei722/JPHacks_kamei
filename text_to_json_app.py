from flask import Flask, request, jsonify, Response
from openai import OpenAI
import json
import os

app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def text_to_json(text: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    system_prompt = """
    あなたは入力された「何かを買った」のようなテキストを正確にJSON形式に変換します。以下の制約に従って変換してください:

    出力仕様:
    1.買われたものが以下のいずれの大カテゴリーに該当するかを判断して
      '日用品', '食品', 'その他'

    2. 必ず以下のJSON形式で出力すること
    {
      "name": 一般名詞のみで構成される文字列とする,
      "quantity": 数値のみ,
      "category": 以下のカテゴリーのいずれかを選択: 
                  '日用品', '食品', 'その他',
      "expiration date": その商品が食品ならば賞味期限、消費期限を一般的なものから推測して書く。その商品が日用品なら一般的になくなりなそう時間を推測してかく。単位は必ず日とすること"
      
      "additional_info": "追加情報を文字列で。ない場合は空文字列"
    }

    3. 厳格な規則：
    - 余計な説明は一切付けない
    - 必ず有効なJSONとして解析可能な形式にする
    - 日本語の文字列はUTF-8でエスケープせずそのまま出力
    - quantity は必ず数値型（文字列にしない）
    - 推測できない情報は null か 空文字列 を使用
    """

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
    print(f"Data received: {data}")
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    result = text_to_json(text)
    
    if not result:
        return jsonify({"error": "Conversion failed"}), 500
    
    # JSONレスポンスの際に日本語文字をそのまま表示するようにする
    response_json = json.dumps(result, ensure_ascii=False)
    return Response(response_json, content_type='application/json; charset=utf-8')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)