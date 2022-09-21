import atexit
import contextlib
import platform

from flask_apscheduler import APScheduler

scheduler = APScheduler()


class ApschedulerConfig:
    SCHEDULER_API_ENABLED = True


def scheduler_init(application):
    """
    保证系统只启动一次定时任务
    :param application: app
    :return:
    """
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        with contextlib.suppress(Exception):
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(application)
            scheduler.start()
            print('Scheduler Started,----------------')

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        with contextlib.suppress(Exception):
            # TODO: 需要注意是，windows在debug=True时启动会报错。有Permission denied问题。debug=False 不会报错。
            #  一般我都是注释掉：msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)即可
            # msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(application)
            scheduler.start()
            print('Scheduler Started,----------------')

        def _unlock_file():
            with contextlib.suppress(Exception):
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)

        atexit.register(_unlock_file)
