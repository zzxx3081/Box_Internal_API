from playwright.sync_api import Playwright, sync_playwright
from termcolor import colored
import os, sys, re, requests, json, urllib3, msvcrt, time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8888',
    'https': 'http://127.0.0.1:8888'
}


# 로그인 진입점
def Authentication() -> dict:
    Box_Login_Class = Box_Account()

    return Box_Login_Class.Essential_Information

def Box_Credential():
    Box_ID = input(colored("Box ID: ", 'yellow'))
    Box_PW = ""
    print(colored("Box PW: ", 'yellow'), end='', flush=True)
    len_Of_PW = 0

    while True:
        pwChar = msvcrt.getch()

        # Case of newline
        if pwChar == b'\r':
            print()
            break

        # Case of backspace
        elif pwChar == b'\b':
            if len_Of_PW < 1:
                pass
            else:
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
                Box_PW = Box_PW[:-1]
                len_Of_PW -= 1

        # [Arrow] Key Exception
        elif pwChar == b'\xe0':
            msvcrt.getch()

        # [Tab] Key Exception
        elif pwChar in [b'\t']:
            continue

        # [Ctrl + z] or [Ctrl + c] -> Shut Down
        elif pwChar in [b'\x03', b'\x1a']:
            print(colored("\n[Shut Down]", 'yellow'))
            sys.exit()

        else:
            print("●", end='', flush=True)
            Box_PW += pwChar.decode("utf-8")
            len_Of_PW += 1

    return Box_ID, Box_PW


class Box_Account:
    def __init__(self):

        Box_ID, Box_PW = Box_Credential()

        self.Essential_Information = {
            'Box ID' : Box_ID,
            'Box PW' : Box_PW,
            'request_token' : "",
            'z' : ""
        }

        self.get_Z()
        self.get_request_token()

    def get_Z(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://account.box.com/login")
            page.type('input[type="text"]', self.Essential_Information['Box ID'])
            page.click("#login-submit")
            page.type('input[type="password"]', self.Essential_Information['Box PW'])
            page.click('#login-submit-password')

            #if 2-factor(SMS or TOTP) 2단계 인증
            if(page.url=="https://account.box.com/login/mfa?redirectUrl=%2Ffolder%2F0"):
                twoCode = input("2단계 인증 코드 : ")
                with page.expect_navigation():
                    page.type('input[type="text"]', twoCode)
                    page.locator("//*[@id=\"app\"]/div[5]/span/div/div[1]/main/div/div/div/form/button").click()
                while(True):
                    if page.url != "https://app.box.com/folder/0":
                        time.sleep(1)
                    else: break
            
            browserCookies = context.cookies()    
            tempZ = next((item for item in browserCookies if item['name']=='z'), None)
            self.Essential_Information['z'] = str(tempZ['value'])

            # z값을 요청에 첨부하기 쉽게 저장
            self.z = {'z' : self.Essential_Information['z']}

            context.close()
            browser.close()

    def get_request_token(self):
        requestURL = "https://app.box.com/folder/0"

        responseData = requests.get(url=requestURL, cookies=self.z, proxies=proxies, verify=False)
        self.Essential_Information['request_token'] = re.search(',\"requestToken\":\"(.+?)\",\"billing\":{', responseData.text).group(1)

        print(colored("cookie z : ", 'yellow'), self.Essential_Information['z'])
        print(colored("request_token : ", 'yellow'), self.Essential_Information['request_token'])