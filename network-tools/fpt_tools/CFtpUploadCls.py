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

    def ftpDisConnect(self):
        self.ftp.close()
