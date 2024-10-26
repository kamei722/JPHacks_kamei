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
    You are an expert in accurately converting input Japanese text to JSON format. Please convert according to the following constraints:
    Output specifications:
    1. output must be in the following JSON format.
    {
    “name": Must be a string consisting of common nouns only. Do not include particles, and classify detailed descriptions in additional_info.
    “quantity": Numerical value only
    “expiration date": The expiration date of the product, inferred from the general one. It should be a specific number of days and the unit should be days.
    “category": Select one of the following categories:. 
                '日用品', '食品', 'その他',.
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

def main():
    # テストケース
    test_texts = [
    "青森県産のりんごを3本買いました"
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