import requests

URL = "https://discord.com/api/webhooks/1492131624702185743/lN_ikLcRtnvdaIs0FouO19FZp0d5RV4__KBOId7sP7FUggOqkpyEUUOj2zVmZQfWOmBU"

def test():
    # ログイン画面ではなく、トップページをシンプルに叩いてみる
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    }
    res = requests.get("https://www.smbcnikko.co.jp/", headers=headers)
    
    if res.status_code == 200:
        requests.post(URL, json={"content": "✅日興の表面（トップページ）にはたどり着きました！次は中に入れるか試します。"})
    else:
        requests.post(URL, json={"content": f"❌トップページすら拒否されました。エラーコード: {res.status_code}"})

if __name__ == "__main__":
    test()
