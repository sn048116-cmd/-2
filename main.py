import os
import requests
from playwright.sync_api import sync_playwright

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
NIKKO_ID = os.environ.get("NIKKO_ID")
NIKKO_PW = os.environ.get("NIKKO_PW")

def send_discord(message, image_path=None):
    payload = {"content": message}
    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                requests.post(DISCORD_WEBHOOK_URL, data=payload, files={"file": f})
        else:
            requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except:
        pass

def check_nikko_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        try:
            # 1. まずログインページにアクセス
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do")
            page.wait_for_timeout(5000) # 5秒待つ

            # 2. 【重要】今の画面を写真に撮って即座にDiscordに送る
            page.screenshot(path="debug_view.png")
            send_discord("【調査】今、日興証券の画面はこうなっています：", "debug_view.png")

            # 3. ID入力欄があるか確認して進む
            if page.query_selector('input[name="ba_id"]'):
                page.fill('input[name="ba_id"]', NIKKO_ID)
                page.fill('input[name="ba_pw"]', NIKKO_PW)
                page.click('button[type="submit"]')
                page.wait_for_timeout(5000)
                page.screenshot(path="after_login.png")
                send_discord("ログイン後の画面です：", "after_login.png")
            else:
                send_discord("ID入力欄が見当たりません。写真を確認して原因を教えてください。")

        except Exception as e:
            send_discord(f"エラーが発生しました: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_nikko_stock()
