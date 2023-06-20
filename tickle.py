import os
import time
import pickle
import random
import platform
from allog.python import pylog
from allog.python.pylog import Level
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# web
damai_url = "https://www.damai.cn/"
# login
login_url = "https://passport.damai.cn/login"
# target
# target_url = "https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_1.591b23e1zTvcwn&id=722910145901"


class Concert:
    def __init__(self, target):
        self.status = 0         # 状态,表示如今进行到何种程度
        self.login_method = 1   # {0:模拟登录,1:Cookie登录}自行选择登录方式
        self.target = target
        self.log = pylog.log(file=None, level=Level.Info)
        current_path = os.getcwd()
        self.log.info(f'current path {current_path}')
        option = webdriver.ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_argument('--disable-blink-features=AutomationControlled')
        try:
            if platform.system().startswith('Windows'):
                driver_path = current_path + '\win\chromedriver.exe'
                self.driver = webdriver.Chrome(executable_path=driver_path, options=option)       # 默认Chrome浏览器
            else:
                self.driver = webdriver.Chrome(options=option)
        except:
            err_msg = '浏览器未找到，请安装Chrome'
            self.log.error(f'init cocert error: {err_msg}')
            raise err_msg

    def set_cookie(self):
        self.driver.get(damai_url)
        time.sleep(random.randint(1, 2))
        self.log.info('###请点击登录###')
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        self.log.info('###请扫码登录###')

        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            sleep(1)
        self.log.info('###扫码成功###')
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        self.log.info('###Cookie保存成功###')
        self.driver.get(self.target)
        time.sleep(random.randint(1, 3))

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            self.log.info('###载入Cookie###')
        except Exception as e:
            self.log.error(f'func get_cookie raise exception: {e}')

    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
            # 载入登录界面
            self.log.info('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
                # 如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(self.target)
                self.get_cookie()
                time.sleep(random.randint(1, 3))

    def enter_concert(self):
        """打开浏览器"""
        self.log.info('###打开浏览器，进入大麦网###')
        # self.driver.maximize_window()           # 最大化窗口
        # 调用登陆
        self.login()                            # 先登录再说
        self.driver.refresh()                   # 刷新页面
        time.sleep(random.randint(1, 3))
        self.status = 2                         # 登录成功标识
        self.log.info('###登录成功###')

    def isElementExist(self, element):
        """判断元素是否存在"""
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag

        except:
            flag = False
            return flag

    def choose_ticket(self):
        """选票操作"""
        if self.status == 2:  # 登录成功入口
            self.log.info('###开始进行日期及票价选择###')
            # 如果跳转到了订单结算界面就算这步成功了，否则继续执行此步
            if self.driver.title.find('确认订单') == -1:
                try:
                    buybutton = self.driver.find_element(By.CLASS_NAME, 'buy-link').text
                    self.log.info('###跳转购票页面###')
                    self.log.info(f'func choose_ticket get buybutton text: {buybutton}')
                    if buybutton == "提交缺货登记":
                        # 改变现有状态
                        self.status = 2
                        self.driver.get(self.target)
                        self.log.info('###抢票未开始，刷新等待开始###')
                        raise
                    elif buybutton == "立即预定":
                        self.driver.find_element(By.CLASS_NAME, 'buybtn').click()
                        # 改变现有状态
                        self.status = 3
                    elif buybutton == "立即购买":
                        self.driver.find_element(By.CLASS_NAME, 'buybtn').click()
                        # 改变现有状态
                        self.status = 4
                    # 选座购买暂时无法完成自动化
                    elif buybutton == "选座购买":
                        self.driver.find_element(By.CLASS_NAME, 'buybtn').click()
                        self.status = 5
                    elif buybutton == '不，立即购买':
                        buylink = self.driver.find_element(By.XPATH, '//div[@class="buy-link"]')
                        buylink.click()
                        # 跳转新页面，通过web网页完成购买
                        self.status = 6
                    else:
                        raise
                except:
                    self.log.error('###未跳转到订单结算界面###')
                    raise "无法结算"
                #这里可能有反爬措施
                # 这里需要等待网页加载完毕，再进行购买
                time.sleep(random.randint(1, 2))
                title = self.driver.title
                self.log.info(f'###get web page title = {title}')
                if title == '选座购买':
                    # 实现选座位购买的逻辑
                    self.choice_seats()
                elif title == '订单确认页':
                    self.log.info('waiting......')
                    if self.driver.find_element(By.CLASS_NAME, 'viewer'):
                        self.log.info('###start check order')
                        self.check_order()
                    else:
                        self.log.error('请添加乘客信息')
                        raise '抢票失败'
                elif title == '确认订单':
                    while True:
                        self.log.info('waiting......')
                        if self.isElementExist('//*[@id="container"]/div/div[9]/button'):
                            self.check_order()
                            break

    def choice_seats(self):
        """选择座位"""
        while self.driver.title == '选座购买':
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img'):
                # 座位手动选择 选中座位之后//*[@id="app"]/div[2]/div[2]/div[1]/div[2]/img 就会消失
                self.log.info('请快速的选择您的座位！！！')
            # 消失之后就会出现 //*[@id="app"]/div[2]/div[2]/div[2]/div
            while self.isElementExist('//*[@id="app"]/div[2]/div[2]/div[2]/div'):
                # 找到之后进行点击确认选座
                self.driver.find_element_by_xpath(
                    '//*[@id="app"]/div[2]/div[2]/div[2]/button').click()

    def check_order(self):
        """下单操作"""
        if self.status in [3, 4, 5, 6]:
            self.log.info('###开始确认订单###')
            try:
                # 选择购票人信息
                # radio = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//div[text()='曹杰']")))
                # radio.click()
                num = 3
                self.log.info(f'Get viewers = {viewers.text}')
                target_i_tag = self.driver.find_element(By.CSS_SELECTOR, f'div.viewer div:nth-child({num}) i')
                self.driver.execute_script("arguments[0].setAttribute('class', 'iconfont icondanxuan-xuanzhong_')", target_i_tag)
            except Exception as e:
                self.log.error('###购票人信息选中失败，自行查看元素位置###')
                self.log.error(f'func check_order got exception: {e}')
            # 最后一步提交订单
            time.sleep(60)  # 太快会影响加载，导致按钮点击无效
            self.driver.find_element_by_xpath(
                '//div[@class = "w1200"]//div[2]//div//div[9]//button[1]').click()

    def finish(self, err):
        """结束"""
        self.log.error(f'Web closed as {err}')
        self.driver.quit()


def ticket_snatch(target):
    try:
        con = None
        con = Concert(target)       # 具体如果填写请查看类中的初始化函数
        con.enter_concert()         # 打开浏览器
        con.choose_ticket()         # 开始抢票

    except Exception as e:
        if con:
            con.finish(e)
