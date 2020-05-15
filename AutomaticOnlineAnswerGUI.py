import PySimpleGUI as sg
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import random
import threading
import requests

cookiesList = []
log_url = 'https://bw.chinahrt.com.cn/#/login'
url = 'https://bw.chinahrt.com.cn/#/'
user = '18762856865'
password = '189154'
data = None

def FetchQuestionData():
    global r
    r = requests.get(
        'https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2020-05-15-%E9%A2%98%E5%BA%93.txt')
    r.encoding = 'gbk'
    global data
    data = r.text.replace('    ', ' ')

def open_browser(url):
    option = webdriver.ChromeOptions()
    option.add_argument('log-level=3')
    driver = webdriver.Chrome(chrome_options=option)
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
        choice_dict[true_answer].click()


def ExclusiveChoice(driver):
    cnt = 0
    while True:
        try:
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
        except:
            print("单选题完成，一共%d道" % (cnt))
            break
    return driver


def MultipleChoice(driver):
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[2]").click()
    time.sleep(2)
    while True:
        try:
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
                else:
                    choice[3].click()
            cnt += 1
            time.sleep(1)
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            time.sleep(1.5)
        except:
            print("多选题完成，一共%d道" % (cnt))
            break

    return driver


def TorF(driver):
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[3]").click()
    time.sleep(2)
    while True:
        try:
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
        except:
            print("判断题完成，一共%d道" % (cnt))
            break
    return driver


def FillTheBlank(driver):
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[4]").click()
    time.sleep(2)
    while True:
        try:
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
        except:
            print("填空题完成，一共%d道" % (cnt))
            break
    return driver


def ShortAnswerQuestions(driver):
    cnt = 0
    driver.find_element_by_xpath("//ul[@class='w1200 m0 oh']/li[5]").click()
    time.sleep(2)
    while True:
        try:
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
        except:
            print("简答题完成，一共%d道" % (cnt))
            break
    return driver


def CaseQuestions(driver):
    cnt = 0
    try:
        driver.find_element_by_xpath(
            "//ul[@class='w1200 m0 oh']/li[6]").click()
        time.sleep(2)
        while True:
            try:
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
            except:
                print("案例题完成，一共%d道" % (cnt))
                break
    except:
        print("没有案例题！")
    return driver



def daydaylearn(num):
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


def FindExclusiveAnswer(question):
    position = data.find(question)
    NewQues = data[position:]
    try:
        ansChoice = NewQues.split("答案：")[1].split("\r")[0]
    except:
        return ' '
    A = NewQues[NewQues.find('A'):][2:].split("\r")[0]
    B = NewQues[NewQues.find('B'):][2:].split("\r")[0]
    C = NewQues[NewQues.find('C'):][2:].split("\r")[0]
    D = NewQues[NewQues.find('D'):][2:].split("\r")[0]
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
    A = NewQues[NewQues.find('A'):][2:].split("\r")[0]
    B = NewQues[NewQues.find('B'):][2:].split("\r")[0]
    C = NewQues[NewQues.find('C'):][2:].split("\r")[0]
    D = NewQues[NewQues.find('D'):][2:].split("\r")[0]
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
    except:
        return None
    return ans


def weekweekpractice():
    driver = open_browser(url)
    for cookie in cookiesList:
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath(
        "//div[@class='he_exam_studying']/ul/li[2]").click()  # 周周练
    time.sleep(2)
    try:
        driver.find_element_by_xpath(
            "//a[@class=' cb btn03_cui cursor Clearfix  m0 ']").click()  # 再来一套
    except:
        try:
            driver.find_element_by_xpath("//a[@class='btn02_cui cursor']").click()  # 继续答题
        except:
            driver.find_element_by_xpath("//a[@class='btn01_cui cursor']").click() # 开始答题
    time.sleep(1.5)
    already_done = [x.text for x in driver.find_elements_by_xpath("//a[@class='tc tip']")]
    not_done = [x.text for x in driver.find_elements_by_xpath("//a[@class='tc']")]
    total_questions = len(already_done) + len(not_done)
    page = 1
    while True:
        time.sleep(0.5)
        if page == (total_questions) + 1:
            print("做完了")
            driver.find_element_by_xpath(
                "//button[@class='el-button btn02_cui el-button--default el-button--small']/span").click()
            time.sleep(1.5)
            driver.find_element_by_xpath(
                "//button[@class='el-button el-button--default el-button--small el-button--primary ']/span").click()
            time.sleep(1.5)
            driver.find_element_by_xpath("//a[@class='btn04_cui '][2]").click()
            break
        if str(page) in already_done:
            page += 1
            print("做过了！")
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
            continue
        page += 1
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
        question = driver.find_element_by_xpath(
            "//div[@class = 'fl'][1]/h1[@class = 'f18']").text  # 题目
        if type_1 == '单选题':
            circleA = driver.find_element_by_xpath("//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dt")
            circleB = driver.find_element_by_xpath("//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dt")
            circleC = driver.find_element_by_xpath("//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dt")
            circleD = driver.find_element_by_xpath("//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dt")
            choiceA = driver.find_element_by_xpath("//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dd").text
            choiceB = driver.find_element_by_xpath("//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dd").text
            choiceC = driver.find_element_by_xpath("//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dd").text
            choiceD = driver.find_element_by_xpath("//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dd").text

            try:
                ans = FindExclusiveAnswer(question)
            except:
                print("找不到答案！")
                random.choice([circleA,circleB,circleC,circleD]).click()
                time.sleep(1)
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == ' ':
                print("第%d题找不到答案！"%(page-1))
                random.choice([circleA, circleB, circleC, circleD]).click()
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
                circleD.click()
        elif type_2 == '多选题':
            circleA = driver.find_element_by_xpath("//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dt")
            circleB = driver.find_element_by_xpath("//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dt")
            circleC = driver.find_element_by_xpath("//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dt")
            circleD = driver.find_element_by_xpath("//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dt")

            choiceA = driver.find_element_by_xpath("//div[@class='fl'][2]/dl[@class='mt20 fl mr40']/dd").text
            choiceB = driver.find_element_by_xpath("//div[@class='fl'][3]/dl[@class='mt20 fl mr40']/dd").text
            choiceC = driver.find_element_by_xpath("//div[@class='fl'][4]/dl[@class='mt20 fl mr40']/dd").text
            choiceD = driver.find_element_by_xpath("//div[@class='fl'][5]/dl[@class='mt20 fl mr40']/dd").text
            try:
                ans = FindMutipleAnswer(question)
            except:
                print("找不到答案！")
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
                print("第%d题找不到答案！" % (page-1))
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
            for c in ans:
                time.sleep(0.5)
                if c == choiceA:
                    circleA.click()
                elif c == choiceB:
                    circleB.click()
                elif c == choiceC:
                    circleC.click()
                else: 
                    circleD.click()
        elif type_3 == '判断题':
            circleA = driver.find_element_by_xpath("//div[@class='fl']/dl[@class='mt20 fl mr40'][1]/dt")
            circleB = driver.find_element_by_xpath("//div[@class='fl']/dl[@class='mt20 fl mr40'][2]/dt")

            choiceA = driver.find_element_by_xpath("//div[@class='fl']/dl[@class='mt20 fl mr40'][1]/dd").text
            choiceB = driver.find_element_by_xpath("//div[@class='fl']/dl[@class='mt20 fl mr40'][2]/dd").text

            try:
                ans = FindTorFAndFillTheBlank(question)
            except:
                print("找不到答案！")
                circleA.click()
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == None:
                print("第%d题找不到答案！" % (page-1))
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
                print("找不到答案！")
                blank[0].send_keys('666666')
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if ans == None:
                print("第%d题找不到答案！" % (page-1))
                blank[0].send_keys('666666')
                try:
                    driver.find_element_by_xpath(
                        "//a[@class='btn04_cui ml20']").click()  # 下一页
                except:
                    break
                continue
            if "；" in ans:
                ansList = ans.split("；")
                cnt = 0
                for i in ansList:
                    blank[cnt].send_keys(i)
                    cnt += 1
            else:
                blank[0].send_keys(ans)
        time.sleep(2)
        try:
            driver.find_element_by_xpath(
                "//a[@class='btn04_cui ml20']").click()  # 下一页
        except:
            break




def GUI():
    sg.ChangeLookAndFeel('GreenTan')

    # ------ Menu Definition ------ #
    # menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
    #             ['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
    #             ['&Help', '&About...'], ]

    # ------ Column Definition ------ #
    column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
            [sg.Spin(values=('Spin Box 1', '2', '3'),
                        initial_value='Spin Box 1')],
            [sg.Spin(values=('Spin Box 1', '2', '3'),
                        initial_value='Spin Box 2')],
            [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

    layout = [
        # [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('全国人社窗口单位业务技能练兵比武——冠军小霸王', size=(
            40, 1), justification='center', font=("Noto Serif SC", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Text('请先登录，登陆时输入验证码，点击登录按钮，只需等待登录页面自动关闭后，再启动其他任务。', size=(
            77, 1), font=("Noto Serif SC", 12),text_color='blue')],
        [sg.Frame('登录选项', [[sg.Text('账号：'),
                           sg.InputText('18912686679', size=(
                               100, 1),key='-USER-')],
        [sg.Text('密码：'),
        sg.InputText('189154', key='-PASSWORD-',size=(
            100, 1))],
            [sg.Button('登录', button_color=('white', 'green'), size=(95, 2))]], font=("Noto Serif SC", 25))],
        [sg.Frame('日日学', [[sg.Button('习近平新时代中国特色社会主义思想、党的十九大精神', font=("Noto Serif SC", 12),button_color=(
            'white', 'red'),size=(40, 2)),
        sg.Button('就业创业', font=("Noto Serif SC", 12),button_color=('white', 'purple'),size=(40, 2))],
        [sg.Button('社会保险', font=("Noto Serif SC", 12),button_color=('white', 'blue'),size=(40, 2)),
        sg.Button('劳动关系', font=("Noto Serif SC", 12),button_color=('black', 'yellow'),size=(40, 2))],
            [sg.Button('人事人才', font=("Noto Serif SC", 12), button_color=('white', 'orange'), size=(40, 2)),
             sg.Button('综合服务标准规范', font=("Noto Serif SC", 12), button_color=(
            'white', 'black'), size=(40, 2))]], font=("Noto Serif SC", 25))],
        [sg.Frame('周周练', [[sg.Button('启动周周练答题进程', font=("Noto Serif SC", 14), button_color=(
            'yellow', 'purple'), size=(70, 2))]], font=("Noto Serif SC", 25))],
        [sg.Frame('月月比', [[sg.Button('启动月月比答题进程', font=("Noto Serif SC", 14), button_color=(
            'white', 'green'), size=(70, 2))]], font=("Noto Serif SC", 25))],
        [sg.Cancel('退出',font=("Consolas", 20), button_color=(
            'white', 'red'), size=(58, 1))]]

    window = sg.Window('自动答题系统', layout,
                    default_element_size=(40, 1), grab_anywhere=False)
    while True:
        event, values = window.read()
        if event == '退出':
            break
        if event == '登录':
            t1 = threading.Thread(
                target=login, args=(str(values['-USER-']), str(values['-PASSWORD-']), log_url))
            t1.start()
        if event == '习近平新时代中国特色社会主义思想、党的十九大精神':
            t2 = threading.Thread(
                target=daydaylearn, args=(1, ))
            t2.start()
        if event == '就业创业':
            t3 = threading.Thread(
                target=daydaylearn, args=(2, ))
            t3.start()
        if event == '社会保险':
            t4 = threading.Thread(
                target=daydaylearn, args=(3, ))
            t4.start()
        if event == '劳动关系':
            t5 = threading.Thread(
                target=daydaylearn, args=(4, ))
            t5.start()
        if event == '人事人才':
            t6 = threading.Thread(
                target=daydaylearn, args=(5, ))
            t6.start()
        if event == '综合服务标准规范':
            t6 = threading.Thread(
                target=daydaylearn, args=(6, ))
            t6.start()
        if event == '启动周周练答题进程':
            t7 = threading.Thread(target=weekweekpractice)
            t7.start()
        # sg.Popup('Title',
        #         'The results of the window.',
        #         'The button clicked was "{}"'.format(event),
        #         'The values are', values)
    window.close()


if __name__ == "__main__":
    t_data = threading.Thread(target=FetchQuestionData)
    t_data.start()
    GUI()
