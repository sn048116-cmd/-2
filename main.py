import os
import requests
from playwright.sync_api import sync_playwright

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
NIKKO_ID = os.environ.get("NIKKO_ID")
NIKKO_PW = os.environ.get("NIKKO_PW")

TARGET_CODES = ["8179"] # ロイホ

def send_discord(message, image_path=None):
    payload = {"content": message}
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            requests.post(DISCORD_WEBHOOK_URL, data=payload, files={"file": f})
    else:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)

def check_nikko_stock():
    with sync_playwright() as p:
        # ブラウザを「人間っぽく」見せる設定を追加
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # ログインページへ移動
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do", wait_until="networkidle")
            
            # 画面が見つからない場合、証拠写真を撮る
            if not page.query_selector('input[name="ba_id"]'):
                page.screenshot(path="error.png")
                send_discord("ログイン画面の入力欄が見つかりません。画面を確認します。", "error.png")
                return

            # 入力
            page.fill('input[name="ba_id"]', NIKKO_ID)
            page.fill('input[name="ba_pw"]', NIKKO_PW)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")

            # 在庫一覧ページへ
            page.goto("https://trade.smbcnikko.co.jp/top/credit_sell_stock_list.do")
            
            for code in TARGET_CODES:
                page.fill('#stock_code', code)
                page.click('#search_button')
                page.wait_for_timeout(2000)

                stock_element = page.query_selector('.stock_count_class')
                if stock_element:
                    count = stock_element.inner_text().replace(',', '')
                    if int(count) > 0:
                        send_discord(f"【日興在庫復活！】\n銘柄: {code}\n在庫数: {count}")
                else:
                    print(f"銘柄 {code} の在庫情報が取得できませんでした。")
                    
        except Exception as e:
            page.screenshot(path="debug.png")
            send_discord(f"エラーが発生しました: {e}", "debug.png")
        finally:
            browser.close()

if __name__ == "__main__":
    check_nikko_stock()
