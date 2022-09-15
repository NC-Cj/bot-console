import datetime
import os
import shutil
import signal
import time

from CFtpUploadCls import CFtpOperCls

bakFilePath = r'e:\bak2022';
srcFilePath = r'd:\data';
isDelSrc = 0;
delayTime = 300;  # 文件上传延时300秒
sleeptime = 5
"""远程文件服务器参数"""
ipaddr = "10.45.44.137";
iPort = 21;
userName = "gmcs_ich_f";
userPwd = "gmcs_ich_f_123";
remorFilePath = r'/ztesoft/gmcs_ich_f'
"""遍历本地目录文件"""
g_isQuit = 1  # 程序运行标识


def getallfilesofwalk(dir):
    """使用listdir循环遍历"""
    fileList = []
    if not os.path.isdir(dir):
        print(dir)
        return
    dirlist = os.walk(dir)
    for root, dirs, files in dirlist:
        for file in files:
            # 如果文件最后修改时间在延迟时间之前，则保存，否则将跳过
            modifyTime = datetime.datetime.fromtimestamp(os.stat(os.path.join(root, file)).st_mtime);
            now = datetime.datetime.now();
            if (now - modifyTime).seconds > delayTime:
                fileList.append(os.path.join(root, file))
                print(os.path.join(root, file))
    return fileList


"""备份文件"""


def bakfile(fileList):
    for i, file in enumerate(fileList):
        if isDelSrc != 0:
            shutil.move(file, bakFilePath)  # 删除源文件
        else:
            shutil.copy(file, bakFilePath)  # 赋值到备份目录


"""捕获信号处理函数"""


def signal_handler(signal, frame):
    print('捕获到异常退出信号:{0}{1}'.format(signal, frame))
    global g_isQuit
    g_isQuit = 0


"""主函数入口"""
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)  # 由Interrupt Key产生，通常是CTRL+C或者DELETE产生的中断
    # signal.signal(signal.SIGHUP, sigintHandler)  # 发送给具有Terminal的Controlling Process，当terminal 被disconnect时候发送
    signal.signal(signal.SIGTERM, signal_handler)  # 请求中止进程，kill命令缺省发送
    ftpUp = CFtpOperCls(ipaddr, iPort, userName, userPwd)
    ftpUp.ftpConnect()
    while (1 == g_isQuit):
        # 获取源目录文件
        fileList = getallfilesofwalk(srcFilePath)
        for i, file in enumerate(fileList):
            ftpUp.uploadFile(file, remorFilePath + '/' + os.path.basename(file))
        bakfile(fileList)  # 备份源目录文件
        print('程序休眠{0}秒'.format(sleeptime))
        time.sleep(sleeptime)
    ftpUp.ftpDisConnect()  # 断开连接
