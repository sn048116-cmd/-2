import os
import requests
from playwright.sync_api import sync_playwright

# あなたのDiscord URL
URL = "https://discord.com/api/webhooks/1492131624702185743/lN_ikLcRtnvdaIs0FouO19FZp0d5RV4__KBOId7sP7FUggOqkpyEUUOj2zVmZQfWOmBU"

def send_discord(msg, img=None):
    try:
        if img:
            with open(img, "rb") as f:
                requests.post(URL, data={"content": msg}, files={"file": f})
        else:
            requests.post(URL, json={"content": msg})
    except: pass

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # ここが「スマホのフリ」をする設定です
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
        )
        page = context.new_page()
        
        try:
            # スマホ用ログインURLに変更しました
            print("ログインページへ移動中...")
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do?v=s")
            page.wait_for_timeout(10000) # 少し長めに待機

            # 今の画面を撮影してDiscordへ送る
            page.screenshot(path="login_view.png")
            send_discord("✅門番を突破できたかな？今の画面です", "login_view.png")

        except Exception as e:
            send_discord(f"エラー発生: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()

