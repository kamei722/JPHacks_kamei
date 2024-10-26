import requests

def test_api():
    # APIのエンドポイント
    url = ""
    
    # テストするテキストの例
    test_texts = [
        "新しいTシャツを3枚まとめ買いした",
        "トイレットペーパーを12個パックで購入",
        "牛乳2本、賞味期限は2024年10月30日まで"
    ]
    
    # ヘッダーの設定
    headers = {
        "Content-Type": "application/json"
    }
    
    # 各テキストでAPIをテスト
    for text in test_texts:
        print(f"\n=== test: {text} ===")
        
        # リクエストの作成と送信
        data = {"text": text}
        response = requests.post(url, json=data, headers=headers)
        
        # レスポンスの表示
        print(f"status: {response.status_code}")
        print("responce:")
        if response.status_code == 200:
            print(json.dumps(response.json(), ensure_ascii=False, indent=2))
        else:
            print(f"error: {response.text}")

if __name__ == "__main__":
    import json
    test_api()