import os
import requests
from playwright.sync_api import sync_playwright

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
NIKKO_ID = os.environ.get("NIKKO_ID")
NIKKO_PW = os.environ.get("NIKKO_PW")

def send_discord(message, image_path=None):
    payload = {"content": message}
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            requests.post(DISCORD_WEBHOOK_URL, data=payload, files={"file": f})
    else:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

def check_nikko_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 画面サイズを大きめにして写真を撮りやすくする
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        try:
            print("日興証券にアクセス中...")
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do")
            
            # 5秒待ってから、まず今の画面を写真に撮る
            page.wait_for_timeout(5000)
            page.screenshot(path="debug_login.png")
            send_discord("【調査中】ログイン画面の状況です。ID入力欄があるか確認してください。", "debug_login.png")

            # ID入力欄を探す
            if page.query_selector('input[name="ba_id"]'):
                page.fill('input[name="ba_id"]', NIKKO_ID)
                page.fill('input[name="ba_pw"]', NIKKO_PW)
                page.click('button[type="submit"]')
                page.wait_for_timeout(5000)
                
                # ログイン後の画面も撮る
                page.screenshot(path="after_login.png")
                send_discord("【調査中】ログイン後の画面です。何かお知らせが出ていませんか？", "after_login.png")
            else:
                send_discord("ID入力欄（ba_id）が見つかりませんでした。送られた写真を確認してください。")

        except Exception as e:
            send_discord(f"エラーが発生しました: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_nikko_stock()
