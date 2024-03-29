import PySimpleGUI as sg
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import random
import threading
import requests
import base64
import os


cookiesList = []
log_url = 'https://bw.chinahrt.com.cn/#/login'
url = 'https://bw.chinahrt.com.cn/#/'
info_url = 'https://bw.chinahrt.com.cn/#/personal/learnStatistics'
user = ''
password = ''
dan_data = None
duo_data = None
pan_data = None
tian_data = None

login_flag = 0
finish_flag = 0
page = 0
img = b'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'
log_driver = None
ansnum = 0
anscnt = 0


def FetchStatistics():
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_opts)
    driver.get(url)
    time.sleep(1)
    for cookie in cookiesList:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    driver.get(info_url)
    time.sleep(1)
    t1 = driver.find_element_by_xpath(
        "//div[@class='module_title_g mb15 question_sum_top']/ul[@class='fr']/li[@class='li1']/p[2]").text
    t2 = driver.find_element_by_xpath(
        "//div[@class='module_title_g mb15 question_sum_top']/ul[@class='fr']/li[@class='li2']/p[2]").text
    t3 = driver.find_element_by_xpath(
        "//div[@class='module_title_g mb15 question_sum_top']/ul[@class='fr']/li[@class='li3']/p[2]").text
    t4 = driver.find_element_by_xpath(
        "//div[@class='module_title_g mb15 question_sum_top']/ul[@class='fr']/li[@class='li4']/p[2]").text

    d1 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][1]/ul[@class='fr']/li[@class='li1']/p").text
    d2 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][1]/ul[@class='fr']/li[@class='li2']/p").text
    d3 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][1]/ul[@class='fr']/li[@class='li3']/p").text
    d4 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][1]/ul[@class='fr']/li[@class='li4']/p").text

    z1 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][2]/ul[@class='fr']/li[@class='li1']/p").text
    z2 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][2]/ul[@class='fr']/li[@class='li2']/p").text
    z3 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][2]/ul[@class='fr']/li[@class='li3']/p").text
    z4 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][2]/ul[@class='fr']/li[@class='li4']/p").text

    y1 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][3]/ul[@class='fr']/li[@class='li1']/p").text
    y2 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][3]/ul[@class='fr']/li[@class='li2']/p").text
    y3 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][3]/ul[@class='fr']/li[@class='li3']/p").text
    y4 = driver.find_element_by_xpath(
        "//div[@class='module_title_g module_title_g2 mb15'][3]/ul[@class='fr']/li[@class='li4']/p").text
    driver.quit()
    return t1, t2, t3, t4, d1, d2, d3, d4, z1, z2, z3, z4, y1, y2, y3, y4


def FetchDanData():
    with open('单选.txt','r') as f:
        r = f.read()
    global dan_data
    dan_data = r.replace('（）', '')
    dan_data = dan_data.replace('()', '')
    dan_data = dan_data.replace('Ｃ', 'C')
    dan_data = dan_data.replace('Ａ', 'A')
    dan_data = dan_data.replace('Ｂ', 'B')
    dan_data = dan_data.replace('Ｄ', 'D')
    dan_data = dan_data.replace('(A)', '')
    dan_data = dan_data.replace('(B)', '')
    dan_data = dan_data.replace('(C)', '')
    dan_data = dan_data.replace('(D)', '')
    dan_data = dan_data.replace('（A）', '')
    dan_data = dan_data.replace('（B）', '')
    dan_data = dan_data.replace('（C）', '')
    dan_data = dan_data.replace('（D）', '')
    dan_data = dan_data.replace('答案:', '答案：')



def FetchDuoData():
    with open('多选.txt','r') as f:
        r = f.read()
    global duo_data
    duo_data = r.replace('（）', '')
    dan_data = duo_data.replace('()', '')
    duo_data = duo_data.replace('Ｃ', 'C')
    duo_data = duo_data.replace('Ａ', 'A')
    duo_data = duo_data.replace('Ｂ', 'B')
    duo_data = duo_data.replace('Ｄ', 'D')
    duo_data = duo_data.replace('答案:','答案：')


def FetchPanData():
    with open('判断.txt','r') as f:
        r = f.read()
    global pan_data
    pan_data = r.replace('（）', '')
    pan_data = pan_data.replace('()', '')
    pan_data = pan_data.replace('Ｃ', 'C')
    pan_data = pan_data.replace('Ａ', 'A')
    pan_data = pan_data.replace('Ｂ', 'B')
    pan_data = pan_data.replace('Ｄ', 'D')
    pan_data = pan_data.replace('答案:', '答案：')

def FetchTianData():
    with open('填空.txt','r') as f:
        r = f.read()
    global tian_data
    tian_data = r.replace('（）', '')
    tian_data = tian_data.replace('()', '')
    tian_data = tian_data.replace('答案:', '答案：')

def open_browser(url):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    return driver


def login(user, password, url):
    global cookiesList
    driver = open_browser(url)
    driver.set_window_size(width=800, height=800, windowHandle="current")
    driver.find_elements_by_class_name('el-input__inner')[0].clear()
    driver.find_elements_by_class_name(
        'el-input__inner')[0].send_keys(user)
    driver.find_elements_by_class_name('el-input__inner')[1].clear()
    driver.find_elements_by_class_name(
        'el-input__inner')[1].send_keys(password)
    while True:
        if driver.find_elements_by_class_name('el-input__inner') == []:
            break
    time.sleep(1)
    driver.refresh()
    cookiesList = driver.get_cookies()
    time.sleep(1)
    global login_flag
    login_flag = 1
    driver.quit()


def ModifyAnswer(driver):
    choice_dict = {}
    error_choice = None
    right_choice = None
    # 不知道是否选对选错，所以可能两种肯定有一种会出错，所有都要用try包起来
    try:
        error_choice = driver.find_element_by_xpath(
            "//span[@class='circle_option fl circle_option_error']/a")
    except:
        pass

    try:
        right_choice = driver.find_element_by_xpath(
            "//ul[@class='option_fl fl']/li[1]/span[@class='circle_option fl circle_option_right']/a")
    except:
        pass

    if error_choice != None:  # 如果选错了，才重新选择
        choice = driver.find_elements_by_xpath(
            "//ul[@class='option_fl fl']/li/span[@class='circle_option fl']/a")
        for i in choice:
            choice_dict[i.text] = i
        true_answer = driver.find_element_by_xpath(
            "//span[@class='f16  right_answer']/span[@class='answer_width']").text
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
              "查看解析，答案错误，由%s改为%s" % (str(error_choice.text), str(true_answer)))
        choice_dict[true_answer].click()


def ExclusiveChoice(driver):
    global anscnt
    global ansnum
    cnt = 0
    try:
        restart_button = driver.find_element_by_xpath(
            "//a[@class='btn04_cui ml20']")
        if restart_button.text == '重新开始':
            restart_button.click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//button[@class = 'el-button el-button--default el-button--small el-button--primary ']").click()
            time.sleep(1)
    except:
        pass
    while True:
        try:
            if anscnt >= ansnum:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练指定%d题完成！" % (ansnum))
                driver.quit()
                break
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "日日练正在做第%d题！" % (anscnt+1))
            choice = driver.find_elements_by_xpath(
                "//ul[@class='option_fl fl']/li/span[@class='circle_option fl']/a")
            random.choice(choice).click()
            cnt += 1
            time.sleep(1)
            ModifyAnswer(driver)
            time.sleep(1)
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            time.sleep(1.5)
            anscnt += 1
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "单选题完成，一共%d道" % (cnt))
            break
    return driver


def MultipleChoice(driver):
    global anscnt
    global ansnum
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[2]").click()
    time.sleep(2)
    try:
        restart_button = driver.find_element_by_xpath(
            "//a[@class='btn04_cui ml20']")
        if restart_button.text == '重新开始':
            restart_button.click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//button[@class = 'el-button el-button--default el-button--small el-button--primary ']").click()
            time.sleep(1)
    except:
        pass
    while True:
        try:
            if anscnt >= ansnum:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练指定%d题完成！" % (ansnum))
                driver.quit()
                break
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "日日练正在做第%d题！" % (anscnt+1))
            # choice_num = random.randint(2, 4)
            choice = driver.find_elements_by_xpath(
                "//ul[@class='option_fl  fl']/li/a/span[@class='circle_option fl']")
            # choiceList = random.sample(choice, choice_num)
            # for c in choiceList:
            #     c.click()
            driver.find_element_by_xpath(
                "//span[@class = 'f20 cursor unl color3e']/a").click()  # 查看解析
            time.sleep(1)
            true_answer = driver.find_element_by_xpath(
                "//span[@class='f16  right_answer']/span[@class='answer_width']").text  # 获取正确答案
            true_choice = str(true_answer).split(",")
            for c in true_choice:
                if c == 'A':
                    choice[0].click()
                elif c == 'B':
                    choice[1].click()
                elif c == 'C':
                    choice[2].click()
                elif c == 'D':
                    choice[3].click()
                else:
                    choice[4].click()
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
                  "查看解析:", " ".join(str(i) for i in true_choice))
            cnt += 1
            time.sleep(1)
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            time.sleep(1.5)
            anscnt += 1
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "多选题完成，一共%d道" % (cnt))
            break

    return driver


def TorF(driver):
    global anscnt
    global ansnum
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[3]").click()
    time.sleep(2)
    try:
        restart_button = driver.find_element_by_xpath(
            "//a[@class='btn04_cui ml20']")
        if restart_button.text == '重新开始':
            restart_button.click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//button[@class = 'el-button el-button--default el-button--small el-button--primary ']").click()
            time.sleep(1)
    except:
        pass
    try:
        restart_button = driver.find_element_by_xpath(
            "//a[@class='btn04_cui ml20']")
        if restart_button.text == '重新开始':
            restart_button.click()
            sp(1)
    except:
        pass
    while True:
        try:
            if anscnt >= ansnum:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练指定%d题完成！" % (ansnum))
                driver.quit()
                break
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "日日练正在做第%d题！" % (anscnt+1))
            choiceTorF = driver.find_elements_by_xpath(
                "//ul[@class = 'option_fl fl']/li/a/span[@class = 'circle_option fl']")
            random.choice(choiceTorF).click()
            time.sleep(1)
            true_answer = driver.find_element_by_xpath(
                "//span[@class = 'f16  right_answer']/span[2]").text
            if true_answer == '正确':
                choiceTorF[0].click()
            else:
                choiceTorF[1].click()
            cnt += 1
            time.sleep(1)
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            time.sleep(1.5)
            anscnt += 1
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "判断题完成，一共%d道" % (cnt))
            break
    return driver


def FillTheBlank(driver):
    global anscnt
    global ansnum
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[4]").click()
    time.sleep(2)
    try:
        restart_button = driver.find_element_by_xpath(
            "//a[@class='btn04_cui ml20']")
        if restart_button.text == '重新开始':
            restart_button.click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//button[@class = 'el-button el-button--default el-button--small el-button--primary ']").click()
            time.sleep(1)
    except:
        pass
    while True:
        try:
            if anscnt >= ansnum:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练指定%d题完成！" % (ansnum))
                driver.quit()
                break
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "日日练正在做第%d题！" % (anscnt+1))
            Blank = driver.find_elements_by_class_name('input_txt')
            # Blank = driver.find_element_by_xpath(
            #     "//span/input[@class= 'input_txt']")
            driver.find_element_by_xpath(
                "//span[@class = 'f20 cursor unl color3e']/a").click()  # 查看解析
            time.sleep(1)
            answer = driver.find_element_by_class_name("answer_width").text
            # answer = driver.find_elements_by_xpath(
            #     "//span[@class='answer_width']").get_attribute('text')
            if len(Blank) > 1:
                answerList = str(answer).split(",")
                for key, _ in enumerate(Blank):
                    Blank[key].send_keys(answerList[key])
            else:
                Blank[0].send_keys(answer)
            time.sleep(2)
            cnt += 1
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            time.sleep(1.5)
            anscnt += 1
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "填空题完成，一共%d道" % (cnt))
            break
    return driver


def ShortAnswerQuestions(driver):
    global anscnt
    global ansnum
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[5]").click()
    time.sleep(2)
    try:
        restart_button = driver.find_element_by_xpath(
            "//a[@class='btn04_cui ml20']")
        if restart_button.text == '重新开始':
            restart_button.click()
            time.sleep(1)
            driver.find_element_by_xpath(
                "//button[@class = 'el-button el-button--default el-button--small el-button--primary ']").click()
            time.sleep(1)
    except:
        pass
    while True:
        try:
            if anscnt >= ansnum:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练指定%d题完成！" % (ansnum))
                driver.quit()
                break
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "日日练正在做第%d题！" % (anscnt+1))
            Blank = driver.find_element_by_xpath(
                "//textarea[@class='mt15 answer_area m0']")
            driver.find_element_by_xpath(
                "//span[@class = 'f20 cursor unl color3e']/a").click()  # 查看解析
            time.sleep(1)
            answer = driver.find_element_by_class_name("answer_width").text
            Blank.send_keys(answer)
            time.sleep(2)
            cnt += 1
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            time.sleep(1.5)
            anscnt += 1
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "简答题完成，一共%d道" % (cnt))
            break
    return driver


def CaseQuestions(driver):
    global anscnt
    global ansnum
    cnt = 0
    try:
        driver.find_element_by_xpath(
            "//ul[@class='w1200 m0 oh']/li[6]").click()
        time.sleep(2)
        try:
            restart_button = driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']")
            if restart_button.text == '重新开始':
                restart_button.click()
                time.sleep(1)
                driver.find_element_by_xpath(
                    "//button[@class = 'el-button el-button--default el-button--small el-button--primary ']").click()
                time.sleep(1)
        except:
            pass
        while True:
            try:
                if anscnt >= ansnum:
                    print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                        time.localtime()), "日日练指定%d题完成！" % (ansnum))
                    driver.quit()
                    break
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练正在做第%d题！" % (anscnt+1))
                Blank = driver.find_element_by_xpath(
                    "//textarea[@class='mt15 answer_area m0']")
                driver.find_element_by_xpath(
                    "//span[@class = 'f20 cursor unl color3e']/a").click()  # 查看解析
                time.sleep(1)
                answer = driver.find_element_by_class_name("answer_width").text
                Blank.send_keys(answer)
                time.sleep(2)
                cnt += 1
                driver.find_element_by_xpath(
                    "//a[@class='btn04_cui ml20']").click()  # 下一页
                time.sleep(1.5)
                anscnt += 1
            except:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "案例题完成，一共%d道" % (cnt))
                break
    except:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "没有案例题！")
    return driver


def daydaylearn(num):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "开始日日学！")
    try:
        driver = open_browser(url)
        for cookie in cookiesList:
            driver.add_cookie(cookie)
        time.sleep(1)
        driver.refresh()
        time.sleep(1)
        driver.find_element_by_xpath(
            "//div[@class='he_exam_studying']/ul/li[1]").click()  # 日日学
        time.sleep(1)
        driver.find_element_by_xpath(
            "//a[@class='btn01_cui cursor mt100']").click()  # 开始答题
        time.sleep(1)
        driver.find_element_by_xpath(
            "//p[@class='cursor'][%s]" % (num)).click()
        driver.switch_to.window(driver.window_handles[-1])  # 切换到新窗口
        time.sleep(1.5)
        driver = ExclusiveChoice(driver)  # 单选
        driver = MultipleChoice(driver)  # 多选
        driver = TorF(driver)  # 判断
        driver = FillTheBlank(driver)
        driver = ShortAnswerQuestions(driver)
        driver = CaseQuestions(driver)
        driver.quit()
    except:
        pass


def FindExclusiveAnswer(question):
    global dan_data
    position = dan_data.find(question)
    NewQues = dan_data[position:]
    try:
        ansChoice = NewQues.split("答案：")[1].split("\n")[0]
    except:
        return ' '
    A = NewQues[NewQues.find('A'):][2:].split("\n")[0].strip().replace(' ', '')
    B = NewQues[NewQues.find('B'):][2:].split("\n")[0].strip().replace(' ', '')
    C = NewQues[NewQues.find('C'):][2:].split("\n")[0].strip().replace(' ', '')
    D = NewQues[NewQues.find('D'):][2:].split("\n")[0].strip().replace(' ', '')
    if ansChoice == 'A':
        ans = A
    elif ansChoice == 'B':
        ans = B
    elif ansChoice == 'C':
        ans = C
    else:
        ans = D
    return ans


def FindMutipleAnswer(question):
    global duo_data
    position = duo_data.find(question)
    NewQues = duo_data[position:]
    try:
        ansChoice = NewQues.split("答案：")[1].split("\n")[0]
    except:
        return []
    A = NewQues[NewQues.find('A'):][2:].split("\n")[0].replace(' ', '')
    B = NewQues[NewQues.find('B'):][2:].split("\n")[0].replace(' ', '')
    C = NewQues[NewQues.find('C'):][2:].split("\n")[0].replace(' ', '')
    D = NewQues[NewQues.find('D'):][2:].split("\n")[0].replace(' ', '')
    try:
        E = NewQues[NewQues.find('E'):][2:].split("\n")[0].replace(' ', '')
    except:
        pass
    try:
        F = NewQues[NewQues.find('F'):][2:].split("\n")[0].replace(' ', '')
    except:
        pass
    try:
        G = NewQues[NewQues.find('G'):][2:].split("\n")[0].replace(' ', '')
    except:
        pass
    ansList = []
    for c in ansChoice:
        if c == 'A':
            ansList.append(A)
        elif c == 'B':
            ansList.append(B)
        elif c == 'C':
            ansList.append(C)
        elif c == 'D':
            ansList.append(D)
        elif c == 'E':
            ansList.append(E)
        elif c == 'F':
            ansList.append(F)
        elif c == 'G':
            ansList.append(G)
    return ansList








def wwpFindTorF(question):
    global pan_data
    position = pan_data.find(question)
    NewQues = pan_data[position:]
    try:
        ans = NewQues.split("答案：")[1].split("\n")[0]
        if '。' in ans:
            ans = ans.replace('。', '')
    except:
        return None
    return ans


def wwpFillTheBlank(question):
    global tian_data
    position = tian_data.find(question)
    NewQues = tian_data[position:]
    try:
        ans = NewQues.split("答案：")[1].split("\n")[0]
        if '。' in ans:
            ans = ans.replace('。', '')
    except:
        return None
    return ans


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def weekweekpractice():
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "开始周周练进程！")
    global page
    driver = open_browser(url)
    for cookie in cookiesList:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath(
        "//div[@class='he_exam_studying']/ul/li[2]").click()  # 周周练
    time.sleep(2)
    button_flag = 0
    try:
        driver.find_element_by_xpath(
            "//a[@class='cb btn03_cui cursor Clearfix m0']").click()  # 再来一套
        button_flag = 1
    except:
        pass
    if button_flag == 0:
        try:
            driver.find_element_by_xpath(
                "//a[@class='btn02_cui cursor']").click()  # 继续答题
            button_flag = 1
        except:
            pass
    if button_flag == 0:
        try:
            driver.find_element_by_xpath(
                "//a[@class='btn01_cui cursor']").click()  # 开始答题
            button_flag = 1
        except:
            pass
    if button_flag == 0:
        try:
            driver.find_element_by_xpath(
                "//a[@class=' cb btn03_cui cursor Clearfix  m0 ']").click()
        except:
            pass

    time.sleep(4)

    already_done = [x.text for x in driver.find_elements_by_xpath(
        "//a[@class='tc tip']")]
    not_done = [x.text for x in driver.find_elements_by_xpath(
        "//a[@class='tc']")]
    total_questions = len(already_done) + len(not_done)
    page = 1
    while True:
        time.sleep(0.5)
        if page == (total_questions) + 1:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "做完了")
            driver.find_element_by_xpath(
                "//button[@class='el-button btn02_cui el-button--default el-button--small']/span").click()
            time.sleep(1.5)
            driver.find_element_by_xpath(
                "//button[@class='el-button el-button--default el-button--small el-button--primary ']/span").click()
            time.sleep(1.5)
            driver.find_element_by_xpath("//a[@class='btn04_cui '][2]").click()
            time.sleep(1)
            global finish_flag
            finish_flag = 1
            break
        if str(page) in already_done:
            page += 1
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "第%d题做过了！" % (page))
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            continue
        page += 1
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "正在做周周练第%d题" % (page-1))
        try:
            type_1 = driver.find_element_by_xpath(
                "//h1[@class='exam_title_cui bg_white pl15 f18'][1]").text[0:3]
        except:
            type_1 = None
        try:
            type_2 = driver.find_element_by_xpath(
                "//h1[@class='exam_title_cui bg_white pl15 f18'][2]").text[0:3]
        except:
            type_2 = None
        try:
            type_3 = driver.find_element_by_xpath(
                "//h1[@class='exam_title_cui bg_white pl15 f18'][3]").text[0:3]
        except:
            type_3 = None
        try:
            type_4 = driver.find_element_by_xpath(
                "//h1[@class='exam_title_cui bg_white pl15 f18'][4]").text[0:3]
        except:
            type_4 = None

        time.sleep(1)
        old_question = driver.find_element_by_xpath(
            "//div[@class = 'fl'][1]/h1[@class = 'f18']").text  # 题目
        old_question = old_question.replace('（）','')
        old_question = old_question.replace('（ ）', '')
        old_question = old_question.replace('()','')
        old_question = old_question.replace('( )','')

        question = ''

        for index, val in enumerate(old_question):
            if index > 0 and index < len(old_question):
                if old_question[index] == ' ' and is_Chinese(old_question[index-1]) and is_Chinese(old_question[index+1]):
                    pass
                else:
                    question += old_question[index]
            else:
                question += old_question[index]
        if '①' in question:
            question.replace('①', '\r\n①')
        

        if type_1 == '单选题':
            circleA = driver.find_element_by_xpath(
                "//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dt")
            circleB = driver.find_element_by_xpath(
                "//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dt")
            circleC = driver.find_element_by_xpath(
                "//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dt")
            try:
                circleD = driver.find_element_by_xpath(
                    "//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dt")
            except:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "没有第四个选项")
                circleD = None

            choiceA = driver.find_element_by_xpath(
                "//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dd").text
            choiceB = driver.find_element_by_xpath(
                "//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dd").text
            choiceC = driver.find_element_by_xpath(
                "//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dd").text
            try:
                choiceD = driver.find_element_by_xpath(
                    "//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dd").text
            except:
                choiceD = ''
            try:
                ans = FindExclusiveAnswer(question)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                random.choice([circleA, circleB, circleC, circleD]).click()
                time.sleep(1)
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == ' ':
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (page-1))
                try:
                    random.choice([circleA, circleB, circleC, circleD]).click()
                except:
                    circleC.click()
                time.sleep(1)
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == choiceA:
                circleA.click()
            elif ans == choiceB:
                circleB.click()
            elif ans == choiceC:
                circleC.click()
            else:
                try:
                    circleD.click()
                except:
                    circleC.click()
        elif type_2 == '多选题':
            circleA = driver.find_element_by_xpath(
                "//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dt")
            circleB = driver.find_element_by_xpath(
                "//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dt")
            circleC = driver.find_element_by_xpath(
                "//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dt")
            try:
                circleD = driver.find_element_by_xpath("//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dt")
            except:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "没有第四个选项")
                circleD = None
            try:
                circleE = driver.find_element_by_xpath("//div[@class='fl'][6]/dl[@class='mt20 fl mr40']/dt")
                choiceE = driver.find_element_by_xpath("//div[@class='fl'][6]/dl[@class='mt20 fl mr40']/dd").text
            except:
                pass
            
            try:
                circleF = driver.find_element_by_xpath("//div[@class='fl'][7]/dl[@class='mt20 fl mr40']/dt")
                choiceF = driver.find_element_by_xpath("//div[@class='fl'][7]/dl[@class='mt20 fl mr40']/dd").text
            except:
                pass

            try:
                circleG = driver.find_element_by_xpath("//div[@class='fl'][8]/dl[@class='mt20 fl mr40']/dt")
                choiceG = driver.find_element_by_xpath("//div[@class='fl'][8]/dl[@class='mt20 fl mr40']/dd").text
            except:
                pass
            
            choiceA = driver.find_element_by_xpath(
                "//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dd").text
            choiceB = driver.find_element_by_xpath(
                "//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dd").text
            choiceC = driver.find_element_by_xpath(
                "//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dd").text
            try:
                choiceD = driver.find_element_by_xpath(
                    "//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dd").text
            except:
                choiceD = ''
            try:
                ans = FindMutipleAnswer(question)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                circleA.click()
                time.sleep(0.5)
                circleB.click()
                time.sleep(0.5)
                circleC.click()
                time.sleep(0.5)
                circleD.click()
                time.sleep(1)
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == []:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (page-1))
                circleA.click()
                time.sleep(0.5)
                circleB.click()
                time.sleep(0.5)
                circleC.click()
                time.sleep(0.5)
                try:
                    circleD.click()
                except:
                    pass
                time.sleep(1)
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            try:
                for c in ans:
                    time.sleep(1)
                    if c == choiceA:
                        circleA.click()
                    elif c == choiceB:
                        circleB.click()
                    elif c == choiceC:
                        circleC.click()
                    elif c == choiceD:
                        circleD.click()
                    elif c == choiceE:
                        circleE.click()
                    elif c == choiceF:
                        circleF.click()
                    elif c == choiceG:
                        circleG.click()
            except:
                random.choice([circleA, circleB, circleC, circleD]).click()
        elif type_3 == '判断题':
            circleA = driver.find_element_by_xpath(
                "//div[@class='fl']/dl[@class='mt20 fl mr40'][1]/dt")
            circleB = driver.find_element_by_xpath(
                "//div[@class='fl']/dl[@class='mt20 fl mr40'][2]/dt")

            choiceA = driver.find_element_by_xpath(
                "//div[@class='fl']/dl[@class='mt20 fl mr40'][1]/dd").text
            choiceB = driver.find_element_by_xpath(
                "//div[@class='fl']/dl[@class='mt20 fl mr40'][2]/dd").text

            try:
                ans = wwpFindTorF(question)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                circleA.click()
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == None:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (page-1))
                circleA.click()
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == choiceA:
                circleA.click()
            else:
                circleB.click()
        else:
            blank = driver.find_elements_by_xpath(
                "//div[@class = 'fl']/dl[@class = 'mt20 fl mr40']/div[@class = 'el-input el-input--small el-input-group el-input-group--prepend']/input[@class = 'el-input__inner']")
            try:
                ans = wwpFillTheBlank(question)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                blank[0].send_keys(' ')
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == None:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (page-1))
                blank[0].send_keys(' ')
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            try:
                if "。" in ans:
                    ans.replace("。", "")
                if "；" in ans:
                    ansList = ans.split("；")
                    cnt = 0
                    for i in ansList:
                        time.sleep(0.5)
                        blank[cnt].send_keys(i)
                        cnt += 1
                elif "、" in ans:
                    ansList = ans.split("、")
                    cnt = 0
                    for i in ansList:
                        time.sleep(0.5)
                        blank[cnt].send_keys(i)
                        cnt += 1
                elif "  " in ans:
                    ansList = ans.split("  ")
                    cnt = 0
                    for i in ansList:
                        time.sleep(0.5)
                        blank[cnt].send_keys(i)
                        cnt += 1
                elif " " in ans:
                    ansList = ans.split(" ")
                    cnt = 0
                    for i in ansList:
                        time.sleep(0.5)
                        blank[cnt].send_keys(i)
                        cnt += 1
                else:
                    blank[0].send_keys(ans)
            except:
                blank[0].clear()
                blank[0].send_keys(ans)
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "明明有2个或者多个括号填空，却只给一个填空，66666真强！")
        time.sleep(2)
        try:
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
        except:
            break


# def monthmonthcompete():


def UpdateData(window):
    global login_flag
    global finish_flag
    while True:
        time.sleep(1)
        if login_flag == 1:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "正在获取历史答题数据...")
            t1, t2, t3, t4, d1, d2, d3, d4, z1, z2, z3, z4, y1, y2, y3, y4 = FetchStatistics()
            window.FindElement("-T1-").update(t1)
            window.FindElement("-T2-").update(t2)
            window.FindElement("-T3-").update(t3)
            window.FindElement("-T4-").update(t4)

            window.FindElement("-D1-").update(d1)
            window.FindElement("-D2-").update(d2)
            window.FindElement("-D3-").update(d3)
            window.FindElement("-D4-").update(d4)

            window.FindElement("-Z1-").update(z1)
            window.FindElement("-Z2-").update(z2)
            window.FindElement("-Z3-").update(z3)
            window.FindElement("-Z4-").update(z4)

            window.FindElement("-Y1-").update(y1)
            window.FindElement("-Y2-").update(y2)
            window.FindElement("-Y3-").update(y3)
            window.FindElement("-Y4-").update(y4)
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "数据刷新成功！")
            login_flag = 0

        if finish_flag == 1:

            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "正在获取历史答题数据...")
            t1, t2, t3, t4, d1, d2, d3, d4, z1, z2, z3, z4, y1, y2, y3, y4 = FetchStatistics()
            window.FindElement("-T1-").update(t1)
            window.FindElement("-T2-").update(t2)
            window.FindElement("-T3-").update(t3)
            window.FindElement("-T4-").update(t4)

            window.FindElement("-D1-").update(d1)
            window.FindElement("-D2-").update(d2)
            window.FindElement("-D3-").update(d3)
            window.FindElement("-D4-").update(d4)

            window.FindElement("-Z1-").update(z1)
            window.FindElement("-Z2-").update(z2)
            window.FindElement("-Z3-").update(z3)
            window.FindElement("-Z4-").update(z4)

            window.FindElement("-Y1-").update(y1)
            window.FindElement("-Y2-").update(y2)
            window.FindElement("-Y3-").update(y3)
            window.FindElement("-Y4-").update(y4)
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "数据刷新成功！")
            finish_flag = 0


def UpdateQuesData(window):
    global page
    while True:
        time.sleep(1)
        window.FindElement("-PROGRESS-").update(page-1)


def transparent_back(img):
    img = img.convert('RGBA')
    L, H = img.size
    color_0 = (255, 255, 255, 255)  # 要替换的颜色
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot, color_1)
    return img


def get_verification_cd(user, password, url, window):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                        time.localtime()), "正在获取验证码...")
    global log_driver
    chrome_opts = webdriver.ChromeOptions()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_opts)
    driver.get(url)
    driver.set_window_size(width=800, height=800, windowHandle="current")
    driver.find_elements_by_class_name('el-input__inner')[0].clear()
    driver.find_elements_by_class_name(
        'el-input__inner')[0].send_keys(user)
    driver.find_elements_by_class_name('el-input__inner')[1].clear()
    driver.find_elements_by_class_name(
        'el-input__inner')[1].send_keys(password)
    # kaptcha_url = driver.find_element_by_id('safecode').get_attribute('src')
    # r = requests.get(kaptcha_url)
    # with open('img.jpg', 'wb') as f:
    #     f.write(r.content)
    # f.close()
    kaptcha = driver.find_element_by_id('safecode')
    kaptcha.screenshot('img.png')
    # img = Image.open('img.jpg')
    # img = transparent_back(img)
    # img.save('imgcode.png')
    with open('img.png', 'rb') as f:
        image = f.read()
    f.close()
    os.remove('img.png')
    # os.remove('imgcode.png')
    base64_data = base64.b64encode(image)
    imgNew = base64_data.decode('utf-8')
    imgNew = bytes(imgNew, encoding="utf8")
    window['safecode'].update(data=imgNew)
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "获取验证码成功！")
    log_driver = driver


def new_login(input_kapcatch):
    global log_driver
    global cookiesList
    log_driver.find_elements_by_xpath(
        "//input[@class='el-input__inner']")[2].send_keys(input_kapcatch)
    log_driver.find_element_by_xpath(
        "//input[@class='logbtn mt40 cursor']").click()
    time.sleep(1)
    if log_driver.find_elements_by_class_name('el-input__inner') == []:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "登录成功！")
        log_driver.refresh()
        cookiesList = log_driver.get_cookies()
        time.sleep(1)
        global login_flag
        login_flag = 1
        log_driver.quit()
    else:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "登录失败，请重新获取验证码！")


def GUI():
    sg.ChangeLookAndFeel('GreenTan')

    # ------ Menu Definition ------ #
    # menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
    #             ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
    #             ['&Help', '&About...'], ]

    # ------ Column Definition ------ #
    sg.theme('Reddit')
    column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
               [sg.Spin(values=('Spin Box 1', '2', '3'),
                        initial_value='Spin Box 1')],
               [sg.Spin(values=('Spin Box 1', '2', '3'),
                        initial_value='Spin Box 2')],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]
    headings = ['正确率', '正确题数', '错误题数', '总题量']
    layout = [
        # [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('全国人社窗口单位业务技能练兵比武——冠军小霸王', size=(
            40, 1), justification='center', font=("Noto Serif SC", 18), relief=sg.RELIEF_RIDGE)],
        [sg.Text('请先获取验证码，进行登录，随后再进行各项进程，可多开。', size=(
            70, 1), font=("Noto Serif SC", 10), text_color='blue')],
        [sg.Frame('登录选项', [[sg.Text('账号：'),
                            sg.InputText('', size=(
                                80, 1), key='-USER-')],
                           [sg.Text('密码：'),
                            sg.InputText('', key='-PASSWORD-', size=(
                                80, 1))], [sg.Frame('验证码', [[sg.Image(data=img, key='safecode'), sg.Button('获取验证码', key='GETCODE'), sg.InputText('', key='CODEBLANK')]]),
                                           sg.Button('登录', button_color=('white', 'green'), size=(8, 4))]], font=("Noto Serif SC", 25), title_color='Tomato')],
        [sg.Frame('日日学', [[sg.Text('设置学习题数：'), sg.InputText('30', key='ANSNUM')], [sg.Button('习中特、党十九大精神', font=("Noto Serif SC", 12), button_color=(
            'white', 'red'), size=(30, 1)),
            sg.Button('就业创业', font=("Noto Serif SC", 12), button_color=('white', 'purple'), size=(30, 1))],
            [sg.Button('社会保险', font=("Noto Serif SC", 12), button_color=('white', 'blue'), size=(30, 1)),
             sg.Button('劳动关系', font=("Noto Serif SC", 12), button_color=('black', 'yellow'), size=(30, 1))],
            [sg.Button('人事人才', font=("Noto Serif SC", 12), button_color=('white', 'orange'), size=(30, 1)),
             sg.Button('综合服务标准规范', font=("Noto Serif SC", 12), button_color=(
                 'white', 'black'), size=(30, 1))]], font=("Noto Serif SC", 25))],
        [sg.Frame('周周练', [[sg.Button('启动周周练答题进程', font=("Noto Serif SC", 14), button_color=(
            'yellow', 'purple'), size=(51, 1))]], font=("Noto Serif SC", 25))],
        [sg.Frame('月月比', [[sg.Button('启动月月比答题进程', font=("Noto Serif SC", 14), button_color=(
            'white', 'green'), size=(51, 1))]], font=("Noto Serif SC", 25))],
        [sg.Text('当前周周练做题进度：'), sg.Text('无数据', size=(3, 1), text_color='pink', font=(
            "Noto Serif SC", 15), relief=sg.RELIEF_RIDGE, key='-PROGRESS-', pad=(0, 0))],
        [sg.Text('  ')] + [sg.Text(h, size=(6, 1), font=("Noto Serif SC", 10))
                           for h in headings],
        [sg.Frame('数据展示', [[sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='blue', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-T1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-T2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-T3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-T4-', pad=(0, 0))]
                                             ], title='汇总情况', title_color='red', relief=sg.RELIEF_SUNKEN, font=("Noto Serif SC", 8), tooltip='Use these to set flags')],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='purple', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-D1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='purple', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-D2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='purple', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-D3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='purple', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-D4-', pad=(0, 0))]
                                             ], title='日日学', title_color='red', relief=sg.RELIEF_SUNKEN, font=("Noto Serif SC", 8), tooltip='Use these to set flags')],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='green', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Z1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='green', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Z2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='green', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Z3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='green', font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Z4-', pad=(0, 0))]
                                             ], title='周周练', title_color='red', relief=sg.RELIEF_SUNKEN, font=("Noto Serif SC", 8), tooltip='Use these to set flags')],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Y1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Y2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Y3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), font=("Noto Serif SC", 8), relief=sg.RELIEF_RIDGE, key='-Y4-', pad=(0, 0))]
                                             ], title='月月比', title_color='red', relief=sg.RELIEF_SUNKEN, font=("Noto Serif SC", 10), tooltip='Use these to set flags')]]), sg.Output(size=(50, 10))],
        [sg.Cancel('退出', font=("Noto Serif SC", 10), button_color=('white', 'red'), size=(5, 1))]]

    window = sg.Window('自动答题系统', layout,
                       default_element_size=(40, 1), grab_anywhere=True, resizable=True, text_justification='center')

    T_data = threading.Thread(target=UpdateData, args=(window,))
    T_data.start()
    T_ques_data = threading.Thread(target=UpdateQuesData, args=(window,))
    T_ques_data.start()
    global ansnum
    while True:
        event, values = window.read()
        ansnum = int(values['ANSNUM'])
        if event == '登录':
            # t1 = threading.Thread(target=login, args=(str(values['-USER-']), str(values['-PASSWORD-']), log_url))
            input_kapcatch = values['CODEBLANK']
            t1 = threading.Thread(target=new_login, args=(input_kapcatch,))
            t1.start()
        elif event == '习中特、党十九大精神':
            t2 = threading.Thread(
                target=daydaylearn, args=(1, ))
            t2.start()
        elif event == '就业创业':
            t3 = threading.Thread(
                target=daydaylearn, args=(2, ))
            t3.start()
        elif event == '社会保险':
            t4 = threading.Thread(
                target=daydaylearn, args=(3, ))
            t4.start()
        elif event == '劳动关系':
            t5 = threading.Thread(
                target=daydaylearn, args=(4, ))
            t5.start()
        elif event == '人事人才':
            t6 = threading.Thread(
                target=daydaylearn, args=(5, ))
            t6.start()
        elif event == '综合服务标准规范':
            t6 = threading.Thread(
                target=daydaylearn, args=(6, ))
            t6.start()
        elif event == '启动周周练答题进程':
            t7 = threading.Thread(target=weekweekpractice)
            t7.start()
        elif event == '启动月月比答题进程':
            # t8 = threading.Thread(target=monthmonthcompete)
            # t8.start()
            pass
        elif event == 'GETCODE':
            t9 = threading.Thread(target=get_verification_cd, args=(
                str(values['-USER-']), str(values['-PASSWORD-']), log_url, window))
            t9.start()
        else:
            break
        # sg.Popup('Title',
        #         'THE RESULTS OF THE WINDOW.',
        #         'THE BUTTON CLICKED WAS "{}"'.FORMAT(EVENT),
        #         'THE VALUES ARE', VALUES)
    window.close()


if __name__ == "__main__":
    dan_data = threading.Thread(target=FetchDanData)
    duo_data = threading.Thread(target=FetchDuoData)
    pan_data = threading.Thread(target=FetchPanData)
    tian_data = threading.Thread(target=FetchTianData)
    dan_data.start()
    duo_data.start()
    pan_data.start()
    tian_data.start()
    GUI()
