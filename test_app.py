import requests
import json

def test_api():
    # APIのエンドポイント
    url = "http://localhost:5000/convert"
    
    # テストするテキストの例
    test_texts = [
        "北海道産の人参を5本買いました",
        # 追加のテストケースを必要に応じてここに追加
    ]
    
    # ヘッダーの設定
    headers = {
        "Content-Type": "application/json"
    }
    
    # 各テキストでAPIをテスト
    for text in test_texts:
        print(f"\n=== Test Input: {text} ===")
        
        # リクエストの作成と送信
        data = {"text": text}
        try:
            response = requests.post(url, json=data, headers=headers)
            
            # ステータスコードの出力
            print(f"HTTP Status Code: {response.status_code}")
            
            # 成功した場合のレスポンス処理
            if response.status_code == 200:
                # JSONレスポンスを整形して表示
                print("Response JSON:")
                print(json.dumps(response.json(), ensure_ascii=False, indent=2))
            else:
                print("Error Response:")
                print(response.text)
                
        except requests.exceptions.RequestException as e:
            # ネットワーク関連のエラーをキャッチ
            print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()