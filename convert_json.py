from openai import OpenAI
import json
import os 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # あなたのAPIキーに置き換えてください

def text_to_json(text: str) -> dict:
    """
    テキストを受け取り、OpenAI GPT-4を使用してJSON形式に変換する関数。
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    # システムメッセージで詳細な指示を与える
    system_prompt = """
あなたは入力されたテキストを正確にJSON形式に変換する専門家です。以下の制約に従って変換してください：

出力仕様:
1. 必ず以下のJSON形式で出力すること
{
  "name": "一般名詞のみで構成される文字列とする 青森のりんごとかはりんごで",
  "quantity": 数値のみ,
  "expiry_date": "YYYY-MM-DD形式で。不明な場合は null",
  "category": "以下のカテゴリーのいずれかを選択: 
              '日用品', '食品', '飲料', '衣類', 'その他'",
  "additional_info": "追加情報を文字列で。ない場合は空文字列"
}

2. 厳格な規則：
- 余計な説明は一切付けない
- 必ず有効なJSONとして解析可能な形式にする
- 日本語の文字列はUTF-8でエスケープせずそのまま出力
- quantity は必ず数値型（文字列にしない）
- 推測できない情報は null か 空文字列 を使用

例：
入力: トイレットペーパー12個セットを買った
出力: {
  "name": "トイレットペーパー",
  "quantity": 12,
  "expiry_date": null,
  "category": "日用品",
  "additional_info": "セット販売"
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
        
        # デバッグ用に生の応答を表示
        print("GPTからの応答:")
        print(json_response)
        print("\n--- 応答終了 ---\n")
        
        return json.loads(json_response)

    except Exception as e:
        print(f"Error converting text to JSON: {e}")
        return {}

def main():
    # テストケース
    test_texts = [
        "新しいTシャツを3枚まとめ買いした"
    ]
    
    for text in test_texts:
        print(f"\n入力テキスト: {text}")
        json_data = text_to_json(text)
        if json_data:
            print("変換されたJSON:")
            print(json.dumps(json_data, ensure_ascii=False, indent=2))
        else:
            print("JSON変換に失敗しました。")

if __name__ == "__main__":
    main()