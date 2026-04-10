import os
import requests
from playwright.sync_api import sync_playwright

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")
NIKKO_ID = os.environ.get("NIKKO_ID")
NIKKO_PW = os.environ.get("NIKKO_PW")

TARGET_CODES = ["8179"] # ロイホ

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
        # 画面サイズを大きくして、ボタンが隠れないようにする
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        try:
            print("日興証券のトップページを開いています...")
            page.goto("https://trade.smbcnikko.co.jp/uap/idp/login/index.do")
            page.wait_for_load_state("networkidle")

            # ログイン画面が出るまで最大10秒待つ。出なければ写真を撮る
            try:
                page.wait_for_selector('input[name="ba_id"]', timeout=10000)
            except:
                print("ログイン画面が見つかりません。現在の画面をDiscordに送ります。")
                page.screenshot(path="debug_screen.png")
                send_discord("【デバッグ】ログイン画面が見つかりません。今の画面はこれです：", "debug_screen.png")
                return

            print("ログイン情報を入力中...")
            page.fill('input[name="ba_id"]', NIKKO_ID)
            page.fill('input[name="ba_pw"]', NIKKO_PW)
            page.click('button[type="submit"]')
            
            # ログイン後の読み込み待ち
            page.wait_for_load_state("networkidle")

            # もし「重要なお知らせ」などの画面が出ていたら写真を撮る
            page.screenshot(path="after_login.png")
            
            print("在庫照会ページへ移動中...")
            page.goto("https://trade.smbcnikko.co.jp/top/credit_sell_stock_list.do")
            page.wait_for_load_state("networkidle")

            for code in TARGET_CODES:
                page.fill('#stock_code', code)
                page.click('#search_button')
                page.wait_for_timeout(2000)

                stock_element = page.query_selector('.stock_count_class')
                if stock_element:
                    count = stock_element.inner_text().replace(',', '')
                    print(f"銘柄 {code} 在庫数: {count}")
                    if int(count) > 0:
                        send_discord(f"【日興在庫復活！】\n銘柄: {code}\n在庫数: {count}")
                else:
                    print(f"銘柄 {code} の在庫が見つかりませんでした。")
                    
        except Exception as e:
            print(f"エラー発生: {e}")
            page.screenshot(path="error_final.png")
            send_discord(f"エラーが発生しました: {e}", "error_final.png")
        finally:
            browser.close()

if __name__ == "__main__":
    check_nikko_stock()
