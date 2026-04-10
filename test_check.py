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
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        try:
            # ログインページへ移動
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do", wait_until="load")
            page.wait_for_timeout(10000) # 10秒じっと待つ
            
            # 【重要】今の画面を写真に撮って送る
            page.screenshot(path="capture.png")
            send_discord("【現在の画面】これを見て原因を判断します", "capture.png")

            # ID入力
            if page.query_selector('input[name="ba_id"]'):
                page.fill('input[name="ba_id"]', ID)
                page.fill('input[name="ba_pw"]', PW)
                page.click('button[type="submit"]')
                page.wait_for_timeout(5000)
                page.screenshot(path="result.png")
                send_discord("ログイン後の画面です", "result.png")
            else:
                send_discord("ID入力欄がありません。写真を確認してください。")
        except Exception as e:
            send_discord(f"エラー: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
