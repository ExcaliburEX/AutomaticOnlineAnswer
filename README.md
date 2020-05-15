<p align="center">
  <a href="" rel="noopener">
 <img width=320 height=200 src="https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2020-05-16-AutoOA.png" alt="Project logo"></a>
</p>

<h3 align="center">AutomaticOnlineAnswer</h3>

<div align="center">

[![HitCount](http://hits.dwyl.com/ExcaliburEX/AutomaticOnlineAnswer.svg)](http://hits.dwyl.com/ExcaliburEX/AutomaticOnlineAnswer)
[![Build Status](https://www.travis-ci.org/ExcaliburEX/AutomaticOnlineAnswer.svg?branch=master)](https://www.travis-ci.org/ExcaliburEX/AutomaticOnlineAnswer)
[![GitHub Issues](https://img.shields.io/github/issues/ExcaliburEX/GHS.svg)](https://github.com/ExcaliburEX/AutomaticOnlineAnswer)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ExcaliburEX/GHS.svg)](https://github.com/ExcaliburEX/AutomaticOnlineAnswer/pulls)
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

![](https://blog-1259799643.cos.ap-shanghai.myqcloud.com/2020-05-16-%E6%88%AA%E5%9B%BE.png)

## 🍓 运行Tips
&emsp;&emsp;每次运行需先点击登录按钮，在自动打开的网页中输入验证码点击页面的“登录”即可，浏览器会自动关闭。后面就可以进行“日日学”，“周周练”。可以进行多开，进行全面加速。

## 🍇 具体程序
&emsp;&emsp;在这里，[AutomaticOnlineAnswerGUI.py](https://github.com/ExcaliburEX/AutomaticOnlineAnswer/blob/V1.0/AutomaticOnlineAnswerGUI.py)。

主要运用了`selenium`来控制网页，用了`pySimpleGUI`制作了GUI。