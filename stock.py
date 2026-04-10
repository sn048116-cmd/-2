import os
import requests
from playwright.sync_api import sync_playwright

# 先ほど成功したURLをここに貼
URL = "https://discord.com/api/webhooks/1492131624702185743/lN_ikLcRtnvdaIs0FouO19FZp0d5RV4__KBOId7sP7FUggOqkpyEUUOj2zVmZQfWOmBU"

# 証券番号（ロイホ：8179）
TARGET_CODES = ["8179"]

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
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()
        try:
            print("ログインページへ移動中...")
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do")
            page.wait_for_timeout(7000) # 画面が出るまで少し待つ

            # ログイン入力欄があるか確認。なければ今の画面を撮る
            if not page.query_selector('input[name="ba_id"]'):
                page.screenshot(path="login_error.png")
                send_discord("【警告】ログイン画面が見つかりません。今の画面を送ります：", "login_error.png")
                return

            # ログイン（Secrets設定がまだ不安なら、ここも直接 ID/PW を書いてもOKです）
            page.fill('input[name="ba_id"]', os.environ.get("NIKKO_ID"))
            page.fill('input[name="ba_pw"]', os.environ.get("NIKKO_PW"))
            page.click('button[type="submit"]')
            page.wait_for_timeout(5000)

            # 在庫画面へ
            page.goto("https://trade.smbcnikko.co.jp/top/credit_sell_stock_list.do")
            page.wait_for_timeout(5000)

            for code in TARGET_CODES:
                page.fill('#stock_code', code)
                page.click('#search_button')
                page.wait_for_timeout(2000)
                
                # 在庫数をチェック（ここは日興の画面仕様に合わせる必要があります）
                page.screenshot(path=f"stock_{code}.png")
                send_discord(f"【チェック完了】{code} の在庫状況です。写真を確認してください：", f"stock_{code}.png")

        except Exception as e:
            page.screenshot(path="error.png")
            send_discord(f"エラー発生: {e}", "error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    run()
