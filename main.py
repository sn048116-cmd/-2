import os
import requests
from playwright.sync_api import sync_playwright

WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
ID = os.environ.get("NIKKO_ID")
PW = os.environ.get("NIKKO_PW")

def send_discord(msg, img=None):
    try:
        if img:
            with open(img, "rb") as f:
                requests.post(WEBHOOK, data={"content": msg}, files={"file": f})
        else:
            requests.post(WEBHOOK, json={"content": msg})
    except: pass

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 人間が操作しているように見せかける設定
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        try:
            # ログインページへ移動
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do")
            page.wait_for_timeout(7000) # 7秒じっと待つ
            
            # 【重要】今見ている画面を写真に撮ってDiscordに送る
            page.screenshot(path="login_check.png")
            send_discord("【現在の画面】これを見てエラーの原因を突き止めます", "login_check.png")

            # ID入力
            if page.query_selector('input[name="ba_id"]'):
                page.fill('input[name="ba_id"]', ID)
                page.fill('input[name="ba_pw"]', PW)
                page.click('button[type="submit"]')
                page.wait_for_timeout(5000)
                page.screenshot(path="after_login.png")
                send_discord("ログイン後の画面です", "after_login.png")
            else:
                send_discord("ID入力欄が見つかりません。写真を確認してください。")
        except Exception as e:
            send_discord(f"エラー発生: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
