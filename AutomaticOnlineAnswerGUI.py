from enum import auto
from sys import flags
from hamcrest import none
import pymysql
import PySimpleGUI as sg
from selenium import webdriver
import time
import random
import threading
import requests
import base64
import os
import sys
from selenium.webdriver.support import \
    expected_conditions as ExpectedConditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import requests
import re

log_url = 'https://bw.rsbsyzx.cn/#/login'
url = 'https://bw.rsbsyzx.cn/#/'
info_url = 'https://bw.rsbsyzx.cn/#/personal/learnStatistics'
user = ''
password = ''
data = None
login_flag = 0
finish_flag = 0
page = 0
img = b'iVBORw0KGgoAAAANSUhEUgAAAH0AAAAyCAYAAABxjtScAAAHgElEQVR4nO2bX0hTbx/AP3Pn6KbTbekstVIzRSr/JEyC1BIh8yKQkCKoLiKKqIu6iSCiLuqiusogIoKiiyCCCsqLMA2LDElSM6mcs2zmlk5dOp2eec55L8K9v/16//Xy1m8v53xgN+Oc53zP83m+3+cPm0FVVRUdTRH3Vweg8/vRpWsQXboG0aVrEF26BtGlaxBdugbRpWsQXboG0aVrEF26BtGlaxBdugbRpWsQXboG0aVrEF26Bvm/la4oCpIkof/w5+cR/uoA/oyqqiiKgsFgAECWZTweDw6Hg+Tk5Mh1brebxsZGDh8+TGFh4Q/tzM7OYjAYMJvNkXb/HdPT0/j9flasWEE4HP7hnqGhIWZnZ1m9ejXT09ORGP94/+joKE6nk8TExJ9+999FzEn3er08f/6cxMREkpKSCAQCXL16lWPHjlFXVweAJElcv36dUChEf38/+fn5GI3GqHbGx8e5ffs2GzZsoKKiAq/Xy6tXrxAEgbi47wXu69evhEIhsrOzAXj37h0ul4t9+/YRDAbx+/34fD76+/vZsWMHPp+PhYUFEhMT6e3txWKxkJSUFHlma2srfX19XLlyRZf+M2RmZlJWVkZTUxO7du1ibGwMk8lEcXEx8L2sNzU14fP5uHjxIq2trTx58oSamhoE4e+vs3z5coqLi7l16xYlJSUsW7aMqqoqjEZjJENv3bqFy+Vi586diKJIZWUlAPHx8ZjNZubn5zl58iQ5OTls2rQpKrO9Xi8PHz7kzJkz2Gw2ANra2igvLyc1NfU39dZ/R0zO6QMDA7S3t2M0GvH5fJjNZux2O4qi0NHRQVtbG2fOnCE9PZ26ujra29u5efMmY2NjKIoCgMFgoLq6mrNnz5KSkoIgCCxZsoSkpCRSUlKwWq2YzWYSEhKwWq1Rn8UpwePx4Ha7qa+vR1VVwuFwJMa3b98iiiIpKSnA98H46dMncnNzowZfLBJz0amqyufPn8nKysJut+P1elmyZAnx8fF0dnbS2trKnj17sFgs+P1+ZFkmJyeHBw8e0NTURH19Pbm5uRiNRlwuF0ajkYaGBsxmM4FAgBs3brBx40acTucPz5ZlGYPBQFxcHLIs09LSQlxcHBMTE9y/f593795x9OhRLBYLHz9+pKSkJJL9U1NTTE9Pk5WV9bu77KeJOemzs7O8f/+elStXEggEcLlcpKen8+LFi0j2Dg8PMzc3R2JiIgsLC6SkpHDkyBEkSSIjI4OEhAQURaGzsxO73R4RI0kSL1++pKysLPLd9PQ0Ho+HcDjM48ePycrKYtu2bQwPD3Pv3j3y8/MpLCwkEAjw+vVrEhISkCSJwcFBqqqqGBsbA75XhWAwSHx8PN3d3WRkZJCenv7DYi8WiLnyLkkSNpuNzMxMBgYGWLduHSaTifPnz7N06VJyc3Opra3F7/eTl5eH0+mkvr6ejo4O5ufnKSkpYe3atRQVFZGamkpaWhqiKEbaFwQBi8UStTsIhULIsozT6SQvL4+pqSm6u7vZtGkTJpMJm81GcnIy8fHxiKLI3NwcxcXFyLJMT08PPT09eL1eGhoaGBkZ4fTp0zx79ixmt5Mxl+k2m40TJ06gKAqyLJOfn4+iKPT29pKWlkZjYyP79+9nfn6eCxcucOrUKbxeL83NzVEZ/GdkWf6HEmw2GwUFBVEDIxAIUFlZSTgcZmJiIur6cDiMIAgcP348asfw5csXVq9ejc1m4+7duxQUFER2CbFGTEmXJInm5mYGBgZISkrC4XDgcDhwu91kZ2djs9mQJIlLly5x4MABzp07x/bt2+nr66O6upqampofOlpVVXw+H4ODg2RmZv5HcSyuxuH7dDM6Osrk5CSKouB2u+nt7cVut2MymSLXud1ujEYja9asYWZmhvT09P9Jn/wKYkq60WjE4XBgtVopLCzEarUSDoe5du0atbW1xMXF4XQ6aWpqYuXKlezduxeTyURfXx8HDx4kISEhqj1VVens7CQYDNLQ0BC1p/5nLFYDg8GAqqqMjo7S3d2N2+1GFEVWrVpFbm4uoihGDbCKigoAnj59isViiTpIijViTnp5eTmTk5N0dXXh9/sZGhpiZGSEsrIyxsfHWb9+PYWFhUxNTbF79266urrIy8tDEATu3LlDfn5+ZFVtMpkYHx+nqqoKRVEYHBxEkiQ8Hg/JycmMj48TDAbp7+9HEARCoRAtLS0UFRVRU1ODyWSitLSULVu2UF5eztatWxFFMWoKkWWZrq4uPB4Psizz8OFDnE5nVBWINQyx+K9VVVUJBAI8evSIN2/esGPHDgoKCmhpaUFRlMjeGCAYDCIIAqIoMjIyQlZWFps3b8ZkMvHt2zdmZmYQBIEPHz4gCAKzs7OYzWYEQWBubg5ZliMVQJZlpqamsNvtlJaWMjMzw8LCAg6H41/GK0kSLpeLy5cvk5GRwaFDh2K6vMek9EUWF1+Lhx1/3EfHIqFQCFEUY/5wJqal6/waYjNldH4punQNokvXILp0DaJL1yC6dA2iS9cgunQNokvXILp0DaJL1yC6dA2iS9cgunQNokvXILp0DaJL1yB/A0IF9UvNpuNHAAAAAElFTkSuQmCC'
automaticDriver = None
ansnum = 0
anscnt = 0
global flag
flag = 1
global chromeDriverLock
chromeDriverLock = None


def FetchStatistics():
    if chromeDriverLock.acquire(blocking=False) == False:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
              "有其它操作进行中，稍后再开始新操作吧！")
        return -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
    else:
        driver = automaticDriver
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
        chromeDriverLock.release()
        return t1, t2, t3, t4, d1, d2, d3, d4, z1, z2, z3, z4, y1, y2, y3, y4


def FetchQuestionData():
    global r
    global flag
    # r = requests.get('https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2020-06-08-%E9%A2%98%E5%BA%93.txt')
    cnt = 1
    while True:
        try:
            r = requests.get(
                'https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2021-5-8-%E9%A2%98%E5%BA%932.txt')
            r.encoding = 'gbk'
            global data
            data = r.text.replace('    ', ' ')
            if '   ' in data:
                data = data.replace('   ', ' ')
            if '  ' in data:
                data = data.replace('  ', ' ')
            data = data.replace('Ｃ', 'C')
            data = data.replace('Ａ', 'A')
            data = data.replace('Ｂ', 'B')
            data = data.replace('Ｄ', 'D')
            break
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
                  "题库获取失败，超过三次建议重启或者更换网络，正在尝试第%d次" % (cnt))
            cnt += 1
            if cnt == 5:
                break
            time.sleep(2)
        if flag == 0:
            break


def open_browser(url):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    return driver


def login(user, password, url):
    if chromeDriverLock.acquire(blocking=False) == False:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
              "有其它操作进行中，稍后再开始新操作吧！")
        return

    driver = open_browser(url)
    driver.set_window_size(width=800, height=1000, windowHandle="current")
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
    time.sleep(1)
    global login_flag
    login_flag = 1
    chromeDriverLock.release()


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
                driver.close()
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
                driver.close()
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
            time.sleep(1)
    except:
        pass
    while True:
        try:
            if anscnt >= ansnum:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "日日练指定%d题完成！" % (ansnum))
                driver.close()
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
                driver.close()
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
                driver.close()
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
                    driver.close()
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
    if chromeDriverLock.acquire(blocking=False) == False:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
              "有其它操作进行中，稍后再开始新操作吧！")
        return

    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "开始日日学！")
    try:
        driver = automaticDriver
        driver.refresh()
        driver.get(url)
        time.sleep(3)
        driver.find_element_by_xpath(
            "//ul[@class='pb30 mt50']/li[1]").click()  # 日日学
        time.sleep(3)
        driver.find_element_by_xpath(
            "//a[@class='btn01_cui cursor mt100']").click()  # 开始答题
        time.sleep(3)
        driver.find_element_by_xpath(
            "//p[@class='cursor'][%s]" % (num)).click()
        driver.switch_to.window(driver.window_handles[-1])  # 切换到新窗口
        time.sleep(3)
        if(anscnt < ansnum):
            driver = ExclusiveChoice(driver)  # 单选
        if(anscnt < ansnum):
            driver = MultipleChoice(driver)  # 多选
        if(anscnt < ansnum):
            driver = TorF(driver)  # 判断
        if(anscnt < ansnum):
            driver = FillTheBlank(driver)
        if(anscnt < ansnum):
            driver = ShortAnswerQuestions(driver)
        if(anscnt < ansnum):
            driver = CaseQuestions(driver)
    except:
        pass
    finally:
        chromeDriverLock.release()


def FindExclusiveAnswer(question):
    position = data.find(question)
    NewQues = data[position:]
    try:
        ansChoice = NewQues.split("答案：")[1].split("\r")[0]
    except:
        return ' '
    A = NewQues[NewQues.find('A'):][2:].split("\r")[0].strip().replace(' ', '')
    B = NewQues[NewQues.find('B'):][2:].split("\r")[0].strip().replace(' ', '')
    C = NewQues[NewQues.find('C'):][2:].split("\r")[0].strip().replace(' ', '')
    D = NewQues[NewQues.find('D'):][2:].split("\r")[0].strip().replace(' ', '')
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
    position = data.find(question)
    NewQues = data[position:]
    try:
        ansChoice = NewQues.split("答案：")[1].split("\r")[0]
    except:
        return []
    A = NewQues[NewQues.find('A'):][2:].split("\r")[0].replace(' ', '')
    B = NewQues[NewQues.find('B'):][2:].split("\r")[0].replace(' ', '')
    C = NewQues[NewQues.find('C'):][2:].split("\r")[0].replace(' ', '')
    D = NewQues[NewQues.find('D'):][2:].split("\r")[0].replace(' ', '')
    ansList = []
    for c in ansChoice:
        if c == 'A':
            ansList.append(A)
        elif c == 'B':
            ansList.append(B)
        elif c == 'C':
            ansList.append(C)
        else:
            ansList.append(D)
    return ansList


def FindTorFAndFillTheBlank(question):
    position = data.find(question)
    NewQues = data[position:]
    try:
        ans = NewQues.split("答案：")[1].split("\r")[0]
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


def monthmonthcompete(flag):
    if chromeDriverLock.acquire(blocking=False) == False:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
              "有其它操作进行中，稍后再开始新操作吧！")
        return

    if flag == 0:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "开始在线PK！")
    else:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "开始人机对战！")

    global page
    driver = automaticDriver
    driver.get(url)
    time.sleep(1)
    driver.refresh()
    WebDriverWait(driver, 15).until(
        ExpectedConditions.presence_of_element_located(
            (By.XPATH, '//div[@id="app"]/section/div[2]/div[2]/ul/li[3]/a/img'))
    )
    driver.find_element_by_xpath(
        '//div[@id="app"]/section/div[2]/div[2]/ul/li[3]/a/img').click()  # 月月比
    time.sleep(4)
    # 确认页面加载完成
    WebDriverWait(driver, 15).until(
        ExpectedConditions.presence_of_element_located(
            (By.XPATH, '//div[@id="app"]/section/div[2]/div[1]/div[2]/img'))
    )
    driver.find_element_by_xpath(
        '//div[@id="app"]/section/div[2]/label/span[1]/span').click()  # 同意活动规则
    time.sleep(0.5)
    if flag == 0:
        driver.find_element_by_xpath(
            "//div[@class='imgText'][1]/img[@class='Clearfix fl mt20']").click()  # pk对战
        time.sleep(1)
        while True:
            try:
                driver.find_element_by_xpath(
                    "//div[@class='selectProvinceArea']/ul[@class='selectProvinceList']/li["+str(random.randint(1, 29))+"]").click()  # 随机选择地区
                break
            except:
                pass

        time.sleep(0.5)
        driver.find_element_by_xpath(
            "//div[@class='mt20 btnBattle tc']/a[@class='continueWait tc']").click()  # 继续按钮
        time.sleep(1)
        try:
            driver.find_element_by_xpath(
                "//div[@class='tc mt20 btnBattle']/a[@class='ml10 rjBattle']").click()  # 转而人机
            print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                time.localtime()), "等不到人，还是人机吧！")
        except:
            pass
    else:
        driver.find_element_by_xpath(
            '//div[@id="app"]/section/div[2]/div[1]/div[2]/img').click()  # 人机对战

    time.sleep(1)
    driver.find_element_by_xpath(
        '//div[@id="app"]/section/div[3]/div/div/div[2]/section/div/div/p[2]/a').click()  # 随机试题
    # 等待第一题加载完成
    WebDriverWait(driver, 15).until(
        ExpectedConditions.presence_of_element_located(
            (By.XPATH, '//div[@id="app"]/section/div[2]/div[3]/div[2]/p[1]'))
    )
    time.sleep(1)

    # 之后进入答题过程，就10道题目，题量都确定的，就别想着while什么的了吧，真的变了再改脚本
    for i in range(10):
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "正在做月月比第%d题" % (i+1))
        questionType = driver.find_element_by_xpath(
            "//div[@class='answerArea mt30']/div[@class='answerType tc']").text[2:5]
        questionContent = driver.find_element_by_xpath(
            "//div[@class='answerArea mt30']/p[@class='answerBattleTitle']").text.replace(' ', '')
        questionContent = str(questionContent)
        questionContent = questionContent.replace('（）', '（ ）')
        questionContent = questionContent.replace("()", "( )")
        if (questionType == '单选题'):
            circleA = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[1]/a/span')
            circleB = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[2]/a/span')
            circleC = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[3]/a/span')
            try:
                circleD = driver.find_element_by_xpath(
                    '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[4]/a/span')
            except:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "没有第四个选项")
                circleD = None

            choiceA = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[1]/p').text
            choiceB = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[2]/p').text
            choiceC = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[3]/p').text
            try:
                choiceD = driver.find_element_by_xpath(
                    '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[4]/p').text
            except:
                choiceD = ''
            try:
                ans = FindExclusiveAnswer(questionContent)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                ans = ' '
            if ans == ' ':
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (i+1))
                try:
                    random.choice([circleA, circleB, circleC, circleD]).click()
                except:
                    circleC.click()
            else:
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
        elif (questionType == '多选题'):
            circleA = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[1]/a/span')
            circleB = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[2]/a/span')
            circleC = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[3]/a/span')
            try:
                circleD = driver.find_element_by_xpath(
                    '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[4]/a/span')
            except:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "没有第四个选项")
                circleD = None
            try:
                circleE = driver.find_element_by_xpath(
                    '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[5]/a/span')
            except:
                circleE = None
            choiceA = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[1]/p').text
            choiceB = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[2]/p').text
            choiceC = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[3]/p').text
            try:
                choiceD = driver.find_element_by_xpath(
                    '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[4]/p').text
            except:
                choiceD = ''
            try:
                choiceE = driver.find_element_by_xpath(
                    '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[5]/p').text
            except:
                choiceE = ''

            try:
                ans = FindMutipleAnswer(questionContent)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                ans = []

            if ans == []:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (i+1))
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
                try:
                    circleE.click()
                except:
                    pass
            else:
                for c in ans:
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
                    time.sleep(0.5)
        elif (questionType == '判断题'):
            circleA = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[1]/a/span')
            circleB = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[2]/a/span')

            choiceA = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[1]/p').text
            if choiceA == "对":
                choiceA = "正确"
            if choiceA == "错":
                choiceA = "错误"
            choiceB = driver.find_element_by_xpath(
                '//div[@id="app"]/section/div[2]/div[3]/div[2]/ul/li[2]/p').text
            if choiceB == "对":
                choiceB = "正确"
            if choiceB == "错":
                choiceB = "错误"

            try:
                ans = FindTorFAndFillTheBlank(questionContent)
            except:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S] ", time.localtime()), "找不到答案！")
                ans = None

            if ans == None:
                print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                                    time.localtime()), "第%d题找不到答案！" % (i+1))
                circleA.click()
            if ans == choiceA:
                circleA.click()
            else:
                circleB.click()
        else:
            # 我也不知道这是什么题，反正不在我预期的单选、多选、判断三种之内，直接下一题吧
            print('发现新题型{0}！'.format(questionType))
        # 下一题
        try:
            driver.find_element_by_xpath(
                "//p[@class='tc mt100']/a/span[@class='nextAnswerBtn']").click()  # 下一页
        except:
            break
        time.sleep(1)
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                        time.localtime()), "月月比完成，请查看成绩！")
    chromeDriverLock.release()


def weekweekpractice():
    if chromeDriverLock.acquire(blocking=False) == False:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()),
              "有其它操作进行中，稍后再开始新操作吧！")
        return

    print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "开始周周练进程！")
    global page
    driver = automaticDriver
    time.sleep(1)
    driver.get(url)
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath(
        "//ul[@class='pb30 mt50']/li[2]").click()  # 周周练
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
                ans = FindTorFAndFillTheBlank(question)
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
                ans = FindTorFAndFillTheBlank(question)
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

    chromeDriverLock.release()


def UpdateData(window):
    print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                        time.localtime()), "正在获取历史答题数据...")
    t1, t2, t3, t4, d1, d2, d3, d4, z1, z2, z3, z4, y1, y2, y3, y4 = FetchStatistics()
    if t1 != -1:
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


def UpdateQuesData(window):
    global flag
    global page
    while True:
        time.sleep(1)
        if flag == 0:
            break
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
    global automaticDriver
    # 重新登录时关闭多余的浏览器窗口
    if automaticDriver != None:
        automaticDriver.close()
        automaticDriver = none

    if user == '' or password == '':
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "请先输入账密！")
        return
    try:
        chrome_opts = webdriver.ChromeOptions()
        # chrome_opts.add_argument("--headless")
        chrome_opts.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
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
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "获取验证码成功！")
        automaticDriver = driver
    except:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "chromedriver没有配置或者需要更新！")


def new_login(input_kapcatch, user):
    automaticDriver.find_elements_by_xpath(
        "//input[@class='el-input__inner']")[2].send_keys(input_kapcatch)
    automaticDriver.find_element_by_xpath(
        "//input[@class='logbtn mt40 cursor']").click()
    time.sleep(1)
    if automaticDriver.find_elements_by_class_name('el-input__inner') == []:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime()), "登录成功！")
        if user != '':
            t_writeuser2mySQL = threading.Thread(
                target=WriteUser2MySQL, args=(user,))
            t_writeuser2mySQL.start()
        automaticDriver.refresh()
        cookiesList = automaticDriver.get_cookies()
        time.sleep(1)
        global login_flag
        login_flag = 1
    else:
        print(time.strftime("[%Y-%m-%d %H:%M:%S] ",
                            time.localtime()), "登录失败，请重新获取验证码！")


def MySQLConnect():
    global flag
    while True:
        try:
            conn = pymysql.connect(
                host='47.96.189.80', port=3306, user="root", passwd="189154", db="AutoOA")
            return conn
        except:
            print(time.strftime("[%Y-%m-%d %H:%M:%S]: ",
                                time.localtime()), '重连数据库中...')
            time.sleep(2)
            try:
                conn.close()
            except:
                pass
        if flag == 0:
            try:
                conn.close()
            except:
                pass
            break


def UpdateOnlineUserNum(window):
    global flag
    old = 0
    while True:
        conn = MySQLConnect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) from user where onlineState='T'")
            res = cursor.fetchone()
            number = res[0]
            window['-USERNUM-'].update(number)
            if number > old:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S]: ", time.localtime()), '当前有%d位学习者加入了战斗！' % (number-old))
            elif number < old:
                print(time.strftime(
                    "[%Y-%m-%d %H:%M:%S]: ", time.localtime()), '当前有%d位学习者离开了战斗~' % (old-number))
            old = number
            cursor.close()
            conn.close()
            time.sleep(3)
        except:
            pass
        if flag == 0:
            break


def GetIP():
    req = requests.get("http://txt.go.sohu.com/ip/soip")
    ip = re.findall(r'\d+.\d+.\d+.\d+', str(req.content))
    return ip[0]


def WriteUser2MySQL(account):
    conn = MySQLConnect()
    cursor = conn.cursor()
    cursor.execute("SELECT * from user where user_account = '%s'" % (account))
    res = cursor.fetchall()
    try:
        ip = GetIP()
    except:
        ip = '6.6.6.6'
    if len(res) == 0:
        cursor.execute("insert into user(user_ip,user_account,onlineState) values('%s','%s','T')" % (
            str(ip), str(account)))
    else:
        cursor.execute("UPDATE user SET user_ip='%s', onlineState='T' WHERE user_account='%s'" % (
            str(ip), str(account)))
    cursor.close()
    conn.commit()
    conn.close()


def UpdateUserInMySQL(account):
    try:
        conn = MySQLConnect()
        cursor = conn.cursor()
        try:
            ip = GetIP()
        except:
            ip = '6.6.6.6'
        cursor.execute("UPDATE user SET user_ip='%s', onlineState='F' WHERE user_account='%s'" % (
            str(ip), str(account)))
        cursor.close()
        conn.commit()
        conn.close()
    except:
        pass


def GUI():
    # sg.ChangeLookAndFeel('GreenTan')

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
        [sg.Text('人社窗口单位业务技能练兵比武V3.8完全版', size=(
            40, 1), justification='center', font=("KaiTi", 18), relief=sg.RELIEF_RIDGE)],
        [sg.Text('请先获取验证码，进行登录，随后再进行各项进程，一次只能运行一项进程。', size=(
            70, 1), font=("KaiTi", 10), text_color='blue')],
        [sg.Text('当前在线用户数：', font=("KaiTi", 12), size=(18, 1)), sg.Text('暂无数据', font=("Comic Sans MS", 12),
                                                                        size=(18, 1), relief=sg.RELIEF_RIDGE, key='-USERNUM-')],
        [sg.Frame('登录选项', [[sg.Text('账号：', font=("KaiTi", 10)),
                            sg.InputText('', size=(
                                80, 1), key='-USER-')],
                           [sg.Text('密码：', font=("KaiTi", 10)),
                            sg.InputText('', key='-PASSWORD-', size=(
                                80, 1))], [sg.Frame('验证码', [[sg.Image(data=img, key='safecode'), sg.Button('获取验证码', key='GETCODE', size=(10, 2), font=("KaiTi", 10)), sg.InputText('', key='CODEBLANK')]], font=("KaiTi", 18)),
                                           sg.Button('登录', font=("KaiTi", 12), button_color=('white', 'green'), size=(8, 4))]], font=("KaiTi", 25), title_color='Tomato')],
        [sg.Frame('日日学', [[sg.Text('设置学习题数：', font=("KaiTi", 10)), sg.InputText('30', key='ANSNUM')], [sg.Button('习中特、党十九大精神', font=("KaiTi", 12), button_color=(
            'white', 'red'), size=(37, 1)),
            sg.Button('就业创业', font=("KaiTi", 12), button_color=('white', 'purple'), size=(37, 1))],
            [sg.Button('社会保险', font=("KaiTi", 12), button_color=('white', 'blue'), size=(37, 1)),
             sg.Button('劳动关系', font=("KaiTi", 12), button_color=('black', 'yellow'), size=(37, 1))],
            [sg.Button('人事人才', font=("KaiTi", 12), button_color=('white', 'orange'), size=(37, 1)),
             sg.Button('综合服务标准规范', font=("KaiTi", 12), button_color=(
                 'white', 'black'), size=(37, 1))]], font=("KaiTi", 25))],
        [sg.Frame('周周练', [[sg.Button('启动周周练答题进程', font=("KaiTi", 14), button_color=(
            'yellow', 'purple'), size=(61, 1))]], font=("KaiTi", 25))],
        [sg.Frame('月月比', [[sg.Button('在线PK', font=("KaiTi", 14), button_color=(
            'white', 'green'), size=(29, 1)), sg.Button('人机对战', font=("KaiTi", 14), button_color=(
                'white', 'orange'), size=(29, 1))]], font=("KaiTi", 25))],
        [sg.Text('当前周周练做题进度：', font=("KaiTi", 10)), sg.Text('无数据', size=(6, 1), text_color='pink', font=(
            "KaiTi", 15), relief=sg.RELIEF_RIDGE, key='-PROGRESS-', pad=(0, 0))],
        # [sg.Text('  ')] + [sg.Text(h, size=(6, 1), font=("KaiTi", 10))
        #                    for h in headings],
        # [sg.Frame('数据展示', [[sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T4-', pad=(0, 0))]
        #                                      ], title='汇总情况', title_color='red', relief=sg.RELIEF_SUNKEN, font=("KaiTi", 8), tooltip='Use these to set flags')],
        [sg.Frame('数据展示', [[sg.Text("  "+h, size=(8, 1), font=("KaiTi", 8), pad=(0, 0))
                            for h in headings],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='blue', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-T4-', pad=(0, 0))]
                                             ], title='汇总情况', title_color='red', relief=sg.RELIEF_SUNKEN, font=("KaiTi", 8), tooltip='Use these to set flags')],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='purple', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-D1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='purple', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-D2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='purple', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-D3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='purple', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-D4-', pad=(0, 0))]
                                             ], title='日日学', title_color='red', relief=sg.RELIEF_SUNKEN, font=("KaiTi", 8), tooltip='Use these to set flags')],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), text_color='green', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Z1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='green', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Z2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='green', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Z3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), text_color='green', font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Z4-', pad=(0, 0))]
                                             ], title='周周练', title_color='red', relief=sg.RELIEF_SUNKEN, font=("KaiTi", 8), tooltip='Use these to set flags')],
                           [sg.Frame(layout=[[sg.Text('无数据', size=(8, 1), font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Y1-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Y2-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Y3-', pad=(0, 0)), sg.Text('无数据', size=(8, 1), font=("KaiTi", 8), relief=sg.RELIEF_RIDGE, key='-Y4-', pad=(0, 0))]
                                             ], title='月月比', title_color='red', relief=sg.RELIEF_SUNKEN, font=("KaiTi", 10), tooltip='Use these to set flags')]], font=("KaiTi", 10)), sg.Output(size=(50, 10))],
        [sg.Button('退出', font=("KaiTi", 10), button_color=('white', 'red'), size=(6, 2)), sg.Button('刷新统计信息', font=("KaiTi", 10), button_color=('white', 'red'), size=(15, 2))]]

    window = sg.Window('自动答题系统V3.7', layout,
                       default_element_size=(40, 1), grab_anywhere=False, resizable=True, text_justification='center', finalize=True)

    global chromeDriverLock
    chromeDriverLock = threading.Lock()
    T_ques_data = threading.Thread(target=UpdateQuesData, args=(window,))
    T_ques_data.start()
    t_OnlineUserNum = threading.Thread(
        target=UpdateOnlineUserNum, args=(window,))
    t_OnlineUserNum.start()
    global ansnum
    while True:
        event, values = window.read()
        ansnum = int(values['ANSNUM'])
        if event == '登录':
            # t1 = threading.Thread(target=login, args=(str(values['-USER-']), str(values['-PASSWORD-']), log_url))
            input_kapcatch = values['CODEBLANK']
            t1 = threading.Thread(target=new_login, args=(
                input_kapcatch, str(values['-USER-'])))
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
        elif event == '在线PK':
            t8 = threading.Thread(target=monthmonthcompete, args=(0, ))
            t8.start()
            pass
        elif event == '人机对战':
            t9 = threading.Thread(target=monthmonthcompete, args=(1, ))
            t9.start()
            pass
        elif event == 'GETCODE':
            t9 = threading.Thread(target=get_verification_cd, args=(
                str(values['-USER-']), str(values['-PASSWORD-']), log_url, window))
            t9.start()
        elif event == sg.WIN_CLOSED or event == 'Exit' or event == '退出':
            UpdateUserInMySQL(str(values['-USER-']))
            global flag
            flag = 0
            sys.exit(0)
            break
        elif event == '刷新统计信息':
            t10 = threading.Thread(target=UpdateData, args=(window,))
            t10.start()
            # sg.Popup('Title',
            #         'THE RESULTS OF THE WINDOW.',
            #         'THE BUTTON CLICKED WAS "{}"'.FORMAT(EVENT),
            #         'THE VALUES ARE', VALUES)


if __name__ == "__main__":
    t_data = threading.Thread(target=FetchQuestionData)
    t_data.start()
    GUI()
