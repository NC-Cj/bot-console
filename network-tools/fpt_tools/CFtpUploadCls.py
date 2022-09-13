from ftplib import FTP


class CFtpOperCls(object):

    def __init__(self, ftpserver, port, usrname, pwd):
        self.ftpserver = ftpserver
        self.port = port
        self.usrname = usrname
        self.pwd = pwd
        self.ftp = self.ftpConnect()

    def ftpConnect(self):
        ftp = FTP()
        try:
            ftp.connect(self.ftpserver, self.port)
            ftp.login(self.usrname, self.pwd)
        except:
            raise IOError('ftp连接失败!!!')
        else:
            print(ftp.getwelcome())
            ftp.set_debuglevel(2)
            return ftp

    def changDir(self, remotePath):
        print('切换到目录{0}'.format(remotePath))
        self.ftp.cwd(remotePath)

    # 下载文件
    def downloadFile(self, ftpfile, localfile):
        bufsize = 1024
        with open(localfile, 'wb') as fid:
            self.ftp.retrbinary('RETR {0}'.format(ftpfile), fid.write, bufsize)
        return True

    # 下载多个文件
    def downloadFiles(self, ftpath, localpath, downlist, downlen):
        print('ftp path: {0}\nlocal path: {1}\n'.format(ftpath, localpath))
        if not os.path.exists(localpath):
            os.makedirs(localpath)
        self.ftp.cwd(ftpath)

        for file in self.ftp.nlst():
            if file.endswith(".zip") and len(downlist) < downlen:
                try:
                    print("下载第{0}/{1}个文件：{2} ,状态：".format(len(downlist) + 1, downlen, file), end='')
                    self.downloadFile(file, os.path.join(localpath, file))
                    downlist.append(file)
                except Exception as err:
                    print(err)
                else:
                    print("successful")
        print("\n下载完成，开始删除服务端文件\n")
        return True

    # 上传文件
    def uploadFile(self, localfile, ftpfile):
        print('local path: {0}\nftp path: {1}\n'.format(localfile, ftpfile))
        bufsize = 1024
        with open(localfile, 'rb') as fid:
            self.ftp.storbinary('STOR {0}'.format(ftpfile), fid, bufsize)

    def ftpdelfile(self, downlist):
        for filedel in downlist:
            try:
                print("删除第{0}/{1}个文件：{2} ,状态：".format(downlist.index(filedel) + 1, downlen, filedel), end='')
                self.ftp.delete(filedel)
            except Exception as err:
                print(err)
            else:
                print("successful")

    def ftpDisConnect(self):
        self.ftp.close()
