# 使用方法

## 支持的微信版本下载 [pc微信客户端](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.6.0.18/WeChatSetup-3.6.0.18.exe)

## 初始化

1. 下载代码后解压

2. 在有`bot.exe`的目录下进入终端，执行`bot init test_robot`

3. 正常情况下初始化命令执行成功会生成了一些机器人启动的文件

## 启动

1. 在有`bot.exe`的目录下进入终端，执行`bot start test_robot`

2. 如果您没有登录pc端微信，他将会弹出登录窗口，扫描即可，随后机器人将管控您的微信
   
   1. 如果您已在pc端登陆，极有可能也会弹出扫码窗口，忽略即可

3. 验证机器人是否成功，在包含被机器人管控的群组中输入`/help`发送，将会收到机器人回复
   
   1. 如果未收到回复，请尝试退出微信以启动机器人后弹出的扫码界面扫码进入

## 结束

1. 在有`bot.exe`的目录下进入终端，执行`bot close`

## 其他自定义

- 可以自定义脚本命令，参考script/spider.py文件格式，同时记得同步修改配置文件（yaml）

- 可以机器人脚本，暂无参考


