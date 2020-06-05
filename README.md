<p align="center">
  <a href="" rel="noopener">
 <img width=320 height=200 src="https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2020-05-16-AutoOA.png" alt="Project logo"></a>
</p>

<h3 align="center">AutomaticOnlineAnswer</h3>

<div align="center">

[![HitCount](http://hits.dwyl.com/ExcaliburEX/AutomaticOnlineAnswer.svg)](http://hits.dwyl.com/ExcaliburEX/AutomaticOnlineAnswer)
[![Build Status](https://www.travis-ci.org/ExcaliburEX/AutomaticOnlineAnswer.svg?branch=master)](https://www.travis-ci.org/ExcaliburEX/AutomaticOnlineAnswer)
[![GitHub Issues](https://img.shields.io/github/issues/ExcaliburEX/AutomaticOnlineAnswer.svg)](https://github.com/ExcaliburEX/AutomaticOnlineAnswer)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ExcaliburEX/AutomaticOnlineAnswer.svg)](https://github.com/ExcaliburEX/AutomaticOnlineAnswer/pulls)
![forks](https://img.shields.io/github/forks/ExcaliburEX/AutomaticOnlineAnswer)
![stars](	https://img.shields.io/github/stars/ExcaliburEX/AutomaticOnlineAnswer)
![repo size](https://img.shields.io/github/repo-size/ExcaliburEX/AutomaticOnlineAnswer)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
</div>

---

# ✨开始
&emsp;&emsp;很简单只需两步，配置好chrome driver，下载[release](https://github.com/ExcaliburEX/AutomaticOnlineAnswer/releases)即可。
## 🍎 Chrome driver 配置
&emsp;&emsp;在chrome的搜索栏输入`chrome://version`查看自己的版本，然后到[chromedriver](http://chromedriver.storage.googleapis.com/index.html)下载对应的chromedriver版本，随便放在哪个文件夹，并把当前文件夹加入到环境变量即可。

## 🍌 下载最新release
&emsp;&emsp;下载[release](https://github.com/ExcaliburEX/AutomaticOnlineAnswer/releases)启动即可，以下是运行界面：

![](https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2020-05-26-%E7%B3%BB%E7%BB%9F%E5%9B%BE.gif)

## 🍓 运行Tips
- 每次运行需先输入账密，然后点击获取验证码，待获取后输入验证码点击登录即可，会有登录成功提示。若由于网络卡顿等原因，导致验证码获取时间较长，请先点击登录后，再重新获取一次验证码。
- 登录成功后，会自动开始抓取历史答题数据，此时无需等待其抓取完毕，可以直接开始答题任务。可以多开，也就是说可以同时开始几个`日日练`任务以及`周周比`任务，并且在达到指定的答题数后，自动关闭所有的`日日练`答题进程。

## 🍇 具体程序
&emsp;&emsp;在这里，[AutomaticOnlineAnswerGUI.py](https://github.com/ExcaliburEX/AutomaticOnlineAnswer/blob/master/AutomaticOnlineAnswerGUI.py)。

主要运用了`selenium`来控制网页，用了`pySimpleGUI`制作了GUI。

# 更新日志
## 🍎 2020-05-17 加入答题数据统计

## 🍉 2020-06-05
- 修改了提示信息的显示，可以显示单选与多选的选择过程
- 修复单选跳过的BUG，以及考虑了多选的E选项
- 加入`日日练`答题数目设置选项，可以设置每日答多少题
- 加入`重新开始`功能，可以自动重新开始已经答完的题目
- 待开发
  - 月月比