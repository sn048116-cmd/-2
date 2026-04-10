import requests

# GitHubのSecretsを使わず、直接URLを指定します
WEBHOOK_URL = "https://discord.com/api/webhooks/1492131624702185743/lN_ikLcRtnvdaIs0FouO19FZp0d5RV4__KBOId7sP7FUggOqkpyEUUOj2zVmZQfWOmBU"

def test_send():https://discord.com/api/webhooks/1492131624702185743/lN_ikLcRtnvdaIs0FouO19FZp0d5RV4__KBOId7sP7FUggOqkpyEUUOj2zVmZQfWOmBU
    print("送信テストを開始します...")
    data = {"content": "✅ なおこさん、届きましたか？これが届けば設定は成功です！"}
    response = requests.post(WEBHOOK_URL, json=data)
    
    if response.status_code == 204:
        print("送信成功！Discordを確認してください。")
    else:
        print(f"送信失敗。エラーコード: {response.status_code}")

if __name__ == "__main__":
    test_send()
