import os
import requests
from playwright.sync_api import sync_playwright

# GitHubの「Secrets」から読み込む設定
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
NIKKO_ID = os.environ.get("NIKKO_ID")
NIKKO_PW = os.environ.get("NIKKO_PW")

# ★監視したい銘柄コードをここに入れてください
TARGET_CODES = ["9202", "8136", "7203"] 

def send_discord(message):
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def check_nikko_stock():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            # ログイン
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do")
            page.fill('input[name="ba_id"]', NIKKO_ID)
            page.fill('input[name="ba_pw"]', NIKKO_PW)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")

            # 在庫一覧ページへ（※ログイン後の正規ルート）
            page.goto("https://trade.smbcnikko.co.jp/top/credit_sell_stock_list.do")

            for code in TARGET_CODES:
                page.fill('#stock_code', code) 
                page.click('#search_button')
                page.wait_for_timeout(2000) # 読み込み待ち

                # 在庫があるか判定（数量が表示される部分を取得）
                stock_element = page.query_selector('.stock_count_class')
                if stock_element:
                    count = stock_element.inner_text().replace(',', '')
                    if int(count) > 0:
                        send_discord(f"【日興在庫復活！】\n銘柄: {code}\n在庫数: {count}\n急いで！")
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    check_nikko_stock()
