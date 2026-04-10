import requests
import sys

# 1. 直接URLを書く（Secretsを使わない）
URL = "https://discord.com/api/webhooks/1492131624702185743/lN_ikLcRtnvdaIs0FouO19FZp0d5RV4__KBOId7sP7FUggOqkpyEUUOj2zVmZQfWOmBU"

def final_test():
    print("送信テスト開始...")
    try:
        # 2. 超シンプルなメッセージ
        res = requests.post(URL, json={"content": "✅なおこさん、これが届いたら通信成功です！"})
        
        # 3. 結果をログに残す（GitHubの画面で見れるようにする）
        if res.status_code == 204:
            print("送信成功しました！Discordを確認してください。")
        else:
            print(f"送信失敗。エラーコード: {res.status_code}")
            print(f"レスポンス内容: {res.text}")
            
    except Exception as e:
        print(f"プログラム実行エラー: {e}")

if __name__ == "__main__":
    final_test()
print("★最新のコードが動いています★")
    
