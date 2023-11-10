import os
import time
import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class WebpageScreenshot:
    def __init__(self, url, driver_path):
        self.init_screenshot_directory()
        self.driver = self.init_webdriver(driver_path)
        self.navigate_to_url(url)
        self.width, self.init_height = 1920, 1800

    def init_screenshot_directory(self):
        # Create a folder named Screenshoot in current path
        self.folder_path = os.path.join(os.getcwd(), 'ScreenShoot1')
        os.makedirs(self.folder_path, exist_ok=True)
        return self.folder_path

    def init_webdriver(self, driver_path):
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--headless")
        service = Service(driver_path)
        try:
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            self.driver.get('about:blank')
            self.driver.execute_script("window.scrollTo(0,0)")
        except Exception as e:
            logging.error(f"Failed to initialize the webdriver: {e}")
            exit(1)
        return self.driver

    def navigate_to_url(self, url):
        self.driver.get(url)
    
    def login(self, email, password):
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{password}\n')
            time.sleep(2)
        except Exception as e:
            logging.error("Login failed with exception: %s", e)
            self.close()
            exit(1)

    def capture_or_next(self, url,xpath, screenshot_filename,next_button):
        self.navigate_to_url(url)
        self.driver.set_window_size(self.width,self.init_height)
        time.sleep(2)

        if next_button[0] == 0:
            self.captuere_screen(xpath, screenshot_filename)
        else:
            self.capture_and_next(xpath, screenshot_filename,next_button[1])

    def resize_window(self,scroll_height):
        # header here has stable height
        if scroll_height>=self.init_height-500:
            self.driver.set_window_size(self.width,scroll_height+500)
            


    def captuere_screen(self,xpath, screenshot_filename):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
            scroll_height = self.driver.execute_script('return arguments[0].scrollHeight;', element)
            self.resize_window(scroll_height)
            self.driver.get_screenshot_as_file(os.path.join(self.folder_path, f"{screenshot_filename}.png"))
            print(scroll_height, f"{screenshot_filename}.png has been saved!")
        except Exception as e:
            logging.error(scroll_height, "Failed to capture element screenshot: %s", e)

    def capture_and_next(self,xpath, screenshot_filename,clickable_ele):
        try:
            # move to the buttom to make the dropdown menu visible
            buttom = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.SBFkwd.mc1cGe')))
            if buttom:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'nearest', inline: 'start'});", buttom)
            else:
                logging.error('No buttom div element here!')
                self.close()
                exit(1)
            # Limit the content into 20 rows, the clickable element is differnet,so it should be marked
            dropdown_child = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, clickable_ele)))
            dropdown_child.click()
            time.sleep(2)

            # select 20/per page in this case
            div_element = dropdown_child.find_element(By.XPATH, '../../..')
            ele_20 = div_element.find_element(By.XPATH, './*[2]/*[2]')
            ele_20.click()
            time.sleep(2)

            img_path = os.path.join(self.folder_path, f"{screenshot_filename}_{0}.png")
            self.driver.get_screenshot_as_file(img_path)
            print(f"{screenshot_filename}_{0}.png has been saved!")
            time.sleep(2)

            idx = 1
            next_click = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".JV3rec .DPvwYc")))
            while next_click and next_click.value_of_css_property('cursor')== 'pointer':
                next_click.click()
                time.sleep(2)
                img_path = os.path.join(self.folder_path, f"{screenshot_filename}_{idx}.png")
                self.driver.get_screenshot_as_file(img_path)
                print(f"{screenshot_filename}_{idx}.png has been saved!")
                next_click = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".JV3rec .DPvwYc")))
                idx += 1
        except Exception as e:
            logging.error("Failed to capture element screenshot: %s", e)
    
    def close(self):
        self.driver.quit()

# Main logic for taking screenshots
def main(email, password, driver_path):
    webpage_screenshot = WebpageScreenshot('https://admin.google.com/', driver_path)
    webpage_screenshot.login(email, password)

    # 2-3-2 not existed in some specific versions
    # '2-3-2 アプリ設定 Chat チャット内でのファイル共有':[('https://admin.google.com/ac/managedsettings/216932279217/filesharingsettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
    urls = {
        '1-1-3 ドメインの管理':[('https://admin.google.com/ac/domains/manage','//div[@class="JAjbAf"]',(0,''))],
        '1-1-4 支払いプラン':[('https://admin.google.com/ac/billing/subscriptions','//section[@class="MDR3f"]',(0,''))],
        '1-2-1 アカウント設定 プロファイル':[('https://admin.google.com/ac/accountsettings/profile','//div[@class="XtA2ub k3Pzib Nw1GEc "]',(0,''))],
        '1-2-2 アカウント設定 設定':[('https://admin.google.com/ac/accountsettings/preferences','//div[@class="chGwx Vy4uEb PBWx0c"]',(0,''))],
        '1-2-3 アカウント設定 スマート機能とパーソナライズ':[('https://admin.google.com/ac/accountsettings/smartfeatures', '//div[@class="chGwx Vy4uEb PBWx0c"]',(0,''))],
        '1-2-4 アカウント設定 カスタマイズ':[('https://admin.google.com/ac/companyprofile/personalization', '//div[@class="chGwx Vy4uEb PBWx0c"]',(0,''))],
        '1-2-5 アカウント設定 追加のデータストレージ':[('https://admin.google.com/ac/companyprofile/supplementaldatastorage', '//div[@class="chGwx Vy4uEb PBWx0c"]',(0,''))],
        '1-2-6 アカウント設定 データ リージョン':[('https://admin.google.com/ac/managedsettings/155680775124/DATA_LOCATION_SETTING', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '1-2-7 アカウント設定 カスタムURL':[('https://admin.google.com/ac/accountsettings/customurl','//div[@class="chGwx Vy4uEb PBWx0c"]',(0,''))],
        '1-3-1 セキュリティ カスタム URL':[('https://admin.google.com/ac/security/passwordmanagement', '//div[@class="chGwx LAx9Gf qi1t7 PBWx0c"]',(0,''))],
        '1-3-2 セキュリティ 安全性の低いアプリ':[('https://admin.google.com/ac/security/lsa', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '1-3-3 セキュリティ 2 段階認証プロセス':[('https://admin.google.com/ac/security/2sv', '//div[@class="chGwx LAx9Gf yukzy PBWx0c"]',(0,''))],
        '1-3-4 セキュリティ アカウントの復元':[('https://admin.google.com/ac/managedsettings/352555445522/accountrecovery', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '1-3-5 セキュリティ ログイン時の本人確認':[('https://admin.google.com/ac/managedsettings/352555445522/loginchallenge', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '1-3-6 セキュリティ 高度な保護機能プログラム':[('https://admin.google.com/ac/managedsettings/352555445522/titanium', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '1-3-7 セキュリティ Google Cloud セッション':[('https://admin.google.com/ac/security/reauth/admin-tools', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-1-1 アプリ設定 コアサービス割り当て':[('https://admin.google.com/ac/appslist/core', '//div[@class="IBCvc"]',(1, ".MocG8c:nth-child(5)"))],
        '2-1-1 アプリ設定 その他アプリ':[('https://admin.google.com/ac/appslist/additional', '//div[@class="IBCvc"]',(1, ".MocG8c:nth-child(5)"))],
        '2-2-1 アプリ設定 Gmail ユーザ設定':[('https://admin.google.com/ac/apps/gmail/usersettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-2-2 アプリ設定 Gmail 安全性':[('https://admin.google.com/ac/apps/gmail/safety', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-2-3 アプリ設定 Gmail 設定':[('https://admin.google.com/ac/apps/gmail/setup','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-2-4 アプリ設定 Gmail エンドユーザーのアクセス':[('https://admin.google.com/ac/apps/gmail/enduseraccess', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-2-5 アプリ設定 Gmail 迷惑メール、フィッシング、マルウェア':[('https://admin.google.com/ac/apps/gmail/spam', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-2-6 アプリ設定 Gmail コンプラアンス':[('https://admin.google.com/ac/apps/gmail/compliance', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-2-7 アプリ設定 Gmail ルーティング':[('https://admin.google.com/ac/apps/gmail/routing', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-1 アプリ設定 Chat チャットの履歴':[('https://admin.google.com/ac/apps/gmail/combinedotrsettings','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
    
        '2-3-3 アプリ設定 Chat スペースの履歴':[('https://admin.google.com/ac/apps/gmail/roomotrsettings','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-4 アプリ設定 Chat Chatの招待':[('https://admin.google.com/ac/managedsettings/216932279217/chatinvitationsettings','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-5 アプリ設定 Chat 外部チャットの設定':[('https://admin.google.com/ac/managedsettings/216932279217/externalchatsettings','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-6 アプリ設定 Chat 外部ユーザー参加のスペース':[('https://admin.google.com/ac/managedsettings/216932279217/guestroomsettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-7 アプリ設定 Chat Chat 用アプリ':[('https://admin.google.com/ac/managedsettings/216932279217/botsettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-8 アプリ設定 Chat GIF':[('https://admin.google.com/ac/managedsettings/216932279217/gifsettings','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-9 アプリ設定 Chat 絵文字オプション':[('https://admin.google.com/ac/managedsettings/216932279217/emojioptions', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-10 アプリ設定 Chat 共有設定':[('https://admin.google.com/ac/managedsettings/216932279217/spacesharingsettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-3-11 アプリ設定 Chat 他のアプリのグループ':[('https://admin.google.com/ac/managedsettings/864450622151/GROUPS_IN_OTHER_APPS','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-4-1 アプリ設定 Meet Meet の動画':[('https://admin.google.com/ac/managedsettings/725740718362/videoSettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-4-2 アプリ設定 Meet Meetの安全性設定':[('https://admin.google.com/ac/managedsettings/725740718362/safetySettings', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-5-1 アプリ設定 カレンダー 共有設定':[('https://admin.google.com/ac/managedsettings/435070579839/sharing', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-5-2 アプリ設定 カレンダー 全般設定':[('https://admin.google.com/ac/managedsettings/435070579839/general', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-5-3 アプリ設定 カレンダー 詳細設定':[('https://admin.google.com/ac/managedsettings/435070579839/advanced', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-5-4 アプリ設定 カレンダー カレンダーの相互運用管理':[('https://admin.google.com/ac/apps/calendar/settings/interop', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-6-1 アプリ設定 ドライブ 共有設定':[('https://admin.google.com/ac/managedsettings/55656082996/sharing', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-6-2 アプリ設定 ドライブ 移行設定':[('https://admin.google.com/ac/managedsettings/55656082996/migrationsettings','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-6-3 アプリ設定 ドライブ 機能とアプリケーション':[('https://admin.google.com/ac/managedsettings/55656082996/data', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-6-4 アプリ設定 ドライブ テンプレート':[('https://admin.google.com/ac/managedsettings/55656082996/docstemplates', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-6-5 アプリ設定 ドライブアクティビティ ダッシュボード':[('https://admin.google.com/ac/managedsettings/55656082996/activitydashboard', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-7-1 アプリ設定 Group 共有設定':[('https://admin.google.com/ac/managedsettings/864450622151/GROUPS_SHARING_SETTINGS_TAB','//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-7-2 アプリ設定 Group 設定':[('https://admin.google.com/ac/managedsettings/864450622151/GROUPS_PREF_SETTINGS_TAB', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '2-7-3 アプリ設定 Group 他のアプリのグループ':[('https://admin.google.com/ac/managedsettings/864450622151/GROUPS_IN_OTHER_APPS', '//div[@class="chGwx LAx9Gf PBWx0c"]',(0,''))],
        '3-2-1 登録 組織部門':[('https://admin.google.com/ac/orgunits', '//div[@class="Bt6j9"]',(0,''))],
        '3-3-3 登録 グループ':[('https://admin.google.com/ac/groups', '//div[@class="gaNcpe VbW90d"]',(1, ".MocG8c:nth-child(2)"))],
    }

    for sheet_name, url_xpath_list in urls.items():
        for idx, (url, xpath,next_button) in enumerate(url_xpath_list, start=1):
            screenshot_filename = f"{sheet_name}"
            webpage_screenshot.capture_or_next(url,xpath, screenshot_filename,next_button)

    webpage_screenshot.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python capture.py <email> <password> <driver_path>")
        exit(1)
    
    main_email = sys.argv[1]
    main_password = sys.argv[2]
    main_driver_path = sys.argv[3]
    main(main_email, main_password, main_driver_path)