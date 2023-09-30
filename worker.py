from selenium.webdriver.support import expected_conditions as EC
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import random, time, threading, sup
from fake_useragent import UserAgent
from VakSmsApi import *
import concurrent.futures

data_list = []
cookie_list = []

class Worker(threading.Thread):
    def __init__(self, name, proxy, mail):
        threading.Thread.__init__(self)
        
        self.sms = VakSmsApi(api_key = '2d9ff5a121b542d3a6dc7c124b9c9fc1')
        self.name = name
        self.mail, self.mailpass = mail.split(':')
        
        selenium_options = {
            'proxy': {
                'http': proxy,
                'https': proxy,
                'no-proxy': 'localhost, 127.0.0.1'
            }
        }
        chrome_preferences = {
            "webrtc.ip_handling_policy" : "disable_non_proxied_udp",
            "webrtc.multiple_routes_enabled": False,
            "webrtc.nonproxied_udp_enabled" : False
        }
        chrome_options = uc.ChromeOptions()
        chrome_options.add_experimental_option("prefs", chrome_preferences)
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-blink-features')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--no-crash-upload")
        chrome_options.add_argument(f"--user-agent={UserAgent(os = 'windows').random}")
        
        self.driver = uc.Chrome(options = chrome_options, seleniumwire_options = selenium_options, headless = True, no_sandbox = False)
        
        tz = {'timezoneId': 'Europe/London'}
        self.driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz)
        print(self.driver.execute_script("return navigator.userAgent"))

    def isExists(self, objectname) -> bool:
        try:
            element = self.driver.find_element(By.XPATH, objectname)
            if (element.is_enabled() and element.is_displayed()):
                element.click()
                return True
            return False
        except:
            return False
    
    def wait(self):
        time.sleep(3)
        while (self.isExists("/html/body/div[1]/div[1]/div[3]")):
            time.sleep(3)

    def run(self):
        try:
            self.driver.get('https://accounts.google.com/signup/v2/createaccount?theme=glif&flowName=GlifWebSignIn&flowEntry=SignUp')
            input_box = self.driver.find_element(By.ID, "firstName")
            input_box.send_keys(self.name)
            button = self.driver.find_element(By.XPATH, "//button")
            button.click()

            self.wait()
            input_box = self.driver.find_element(By.ID, "day")
            input_box.send_keys(str(random.randint(1, 29)))
            input_box = self.driver.find_element(By.ID, "year")
            input_box.send_keys(str(random.randint(1970, 2005)))
            selector = self.driver.find_element(By.XPATH, "//select[@id='month']/option[@value='"+str(random.randint(1, 12))+"']")
            selector.click()
            selector = self.driver.find_element(By.XPATH, "//select[@id='gender']/option[@value='3']")
            selector.click()
            button = self.driver.find_element(By.XPATH, "//button")
            button.click()

            self.wait()
            username = self.name+str(random.randint(1000000,99999999))
            if (self.isExists("//input")):
                input_box = self.driver.find_element(By.XPATH, "//input")
                input_box.send_keys(username)
                username += '@gmail.com'
            else:
                selector = self.driver.find_element(By.XPATH, '//div[@tabindex="0"]')
                username = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/span/div[1]/div/div[2]/div[1]/div').text
                selector.click()
            button = self.driver.find_element(By.XPATH, "//button")
            button.click()

            self.wait()
            password = sup.passgen()
            input_box = self.driver.find_element(By.XPATH, "//input[@name='Passwd']")
            input_box.send_keys(password)
            input_box = self.driver.find_element(By.XPATH, "//input[@name='PasswdAgain']")
            input_box.send_keys(password)
            button = self.driver.find_element(By.XPATH, "//button")
            button.click()

            self.wait()
            input_box = self.driver.find_element(By.XPATH, "//input[@id='phoneNumberId']")
            number = self.sms.get_number(service = 'gl', country = 'gb', operator = 'o2')
            input_box.send_keys(number['tel'])
            button = self.driver.find_element(By.XPATH, "//button")
            button.click()
            
            self.wait()
            if (not self.isExists("//input[@id='code']")):
                self.sms.change_status(idNum=number['idNum'], status='bad')
                print('Номер забанен')
                self.driver.quit()
                return
            time.sleep(60)
            try:
                answer = self.sms.get_sms(number['idNum'])
            except:
                self.sms.change_status(idNum=number['idNum'], status='bad')
                print("Не получил ответа по истечении минуты")
            print(answer)
            input_box = self.driver.find_element(By.XPATH, "//input[@id='code']")
            input_box.send_keys(answer['smsCode'])
            button = self.driver.find_element(By.XPATH, "//button")
            button.click()

            self.wait()
            button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/button")
            button.click()
            

            self.wait()
            button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div/div[2]/div/div/button")
            button.click()          

            self.wait()
            button = self.driver.find_element(By.XPATH, "//*[@id='next']/div")
            button.click()

            self.wait()
            if (self.isExists("//form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]/div")):
                check_box = self.driver.find_element(By.XPATH, "//form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]/div")
                check_box.click()
                button = self.driver.find_element(By.XPATH, "//div[2]/div[2]/div/div[2]/div/div/div/div/button")
                button.click()
                self.wait()
                button = self.driver.find_element(By.XPATH, "//div[2]/div[2]/div/div[2]/div/div/div[2]/div/div/button")
                button.click()
            
            self.wait()
            button = self.driver.find_element(By.XPATH, "//div[2]/div[2]/div/div[2]/div/div[1]/div/div/button")
            button.click()
                
            self.wait()
            original_window = self.driver.current_window_handle
            self.driver.get('https://mail.google.com/mail/u/0/#settings/fwdandpop')
            button = self.driver.find_element(By.XPATH, '//*[@id=":3h"]/input')
            button.click()
            input_box = self.driver.find_element(By.XPATH, '//*[@id=":3a"]')
            input_box.send_keys(self.mail)
            button = self.driver.find_element(By.XPATH, '/html/body/div[22]/div[3]/button[1]')
            for window_handle in self.driver.window_handles():
                if window_handle != original_window:
                    self.driver.switch_to.window(window_handle)
            button.click()
            button = self.driver.find_element(By.XPATH, '/html/body/form/table/tbody/tr/td/input[3]')
            self.driver.switch_to.window(original_window)
            time.sleep(60)
            self.driver.get(sup.email_link(self.mail, self.mailpass))
            button = self.driver.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td/form/p/input')
            button.click()
            time.sleep(1)
            self.driver.get('https://mail.google.com/mail/u/0/#settings/fwdandpop')
            self.driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[6]/div/table/tbody/tr[1]/td[2]/div/div[1]/table[2]/tbody/tr/td[1]/input').click()
            
            self.sms.change_status(idNum=number['idNum'], status='end')
            cookie  = self.driver.get_cookies()
            data_list.append(username+':'+password+'\n')
            cookie_list.append(cookie+'\n')
            self.driver.quit()
            print('Поток завершил свою работу')
        except:
            try:
                self.sms.change_status(idNum=number['idNum'], status='bad')
                print('Номер вернули')
            except:
                print('Номер не выдавали')
            self.driver.quit()
            print('Поток завершился неудачно')
            raise Exception()
        
def run(proxy_list, mail_list):
    name_list = sup.parse('names.txt')
    for i in range(10):
        t = Worker(random.choice(name_list), proxy_list[i], mail_list[i])
        t.start()
    with open("logpass.txt", "a") as f:
        f.writelines(data_list)
    with open("cookie.txt", "a") as f:
        f.writelines(cookie_list)
    return cookie_list, proxy_list

# def run(proxy_list, mail_list):
#     name_list = sup.parse('names.txt')
#     with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#         futures = []
#         for i in range(10):
#             name = random.choice(name_list)
#             proxy = proxy_list[i]
#             mail  = mail_list[i]
#             future = executor.submit(run, name, proxy, mail)
#             futures.append(future)
#         concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
#     with open("logpass.txt", "a") as f:
#         f.writelines(data_list)
#     with open("cookie.txt", "a") as f:
#         f.writelines(cookie_list)
#     return cookie_list, proxy_list
    
    
if __name__ == "__main__":
    run(proxy_list=sup.parse('proxy.txt'), mail_list=sup.parse('mail.txt'))