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
    要求されるJSON形式は以下の通りです:
    request: {
    "item": {
        "display_name": "入力テキストに基づく表示名をそのまま使用します",
        "generic_name": "入力テキストの生成される一般名を助詞を含めずに使用",
        "status": "unpacked"  # 常に'unpacked'に設定
        "user_id": <送られてきたuser_idを使用>
    },
    "shelf_life_days": <一般的な賞味期限を日単位で推測して設定。該当しないものの場合はは空>,
    "category_names": <第一要素が 'Food', 'daily necessities', 'others'のいずれか。残りの要素には自由に追加情報を含めます>
    }

    具体的な変換例:
    - テキストから取得する名詞指示に基づき `display_name`と`generic_name`を定義します。
    - `user_id`は入力データに直接与えられます。
    - `shelf_life_days`は食品の一般的な賞味期限を推測して設定します。該当しない場合は空としておきます。
    - `category_names`は項目の大カテゴリーを最初の要素として設定し、その他の要素として追加情報を含みます。

    厳格な規則:
    - 余計な説明は一切付けない
    - 必ず有効なJSONとして解析可能な形式にする
    - すべてのフィールドは指定されたルールに従って埋めること

    例 
    入力: user_id: 4  "長野県産のキャベツを1玉買った"
    出力:
    request: {
    "item": {
        "display_name": "長野県産のキャベツ",
        "generic_name": "キャベツ",
        "status": "unpacked"  # 常に'unpacked'に設定
        "user_id": 4
    },
    "shelf_life_days": 7,
    "category_names": ["Food", "野菜", "長野県産"]
    }
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