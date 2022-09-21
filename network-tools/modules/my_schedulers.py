import atexit
import contextlib
import datetime
import os
import platform

from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError
from flask_apscheduler import APScheduler

from config import ScapyTable, RecordTable, docker_, TZ, CONTAINER_LOG_PATH, S3, LOG_BUCKET
from modules import app
from modules.tools import to_format, get_write_db_state

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


@scheduler.task('interval', id='do_update_state', seconds=5)
def update_state():
    global db_state, filename
    try:
        now = datetime.datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')
        rows = ScapyTable.get_mac()
        for row in rows:
            name = to_format(row[1])
            containers = docker_.docker_find_container({"name": name})

            if containers is False:
                continue

            code, status = docker_.get_docker_container_status(containers)
            app.logger.info(f'容器状态: {code}-{status}')

            db_state, filename = get_write_db_state(code, containers, status)

            if isinstance(filename, bool):
                continue

            if db_state is None:
                raise AssertionError("db_state is not allowed to be equal to 'None'")

            if db_state != row[2]:  # update to scapy table
                app.logger.info(f'MAC地址:{row[1]}, 数据库状态:{row[2]}, 容器状态码:{code}, 容器状态:{status}, 更新到db状态:{db_state}')
                ScapyTable.scapy_update('burn_state', 'mac', row[1], db_state)

                if db_state in ['烧录成功', '写号成功', '烧录异常', '写号异常', '烧录已取消', '写号已取消']:
                    RecordTable.insert_record(
                        {
                            "ip": row[0],
                            "mac": row[1],
                            "state": db_state,
                            "record_time": now,
                            "log_name": filename
                        }
                    )
    except AssertionError:
        app.logger.error(f'烧录、写号得到更改数据库状态是: {db_state}，应该产生的日志文件是: {filename}')
    except Exception as e:
        app.logger.exception(f'update_state Exception: {e}')


@scheduler.task('interval', id='do_upload_logs', seconds=60)
def upload_logs():
    try:
        dir_list = os.listdir(CONTAINER_LOG_PATH)
    except FileNotFoundError:
        os.makedirs(CONTAINER_LOG_PATH, exist_ok=True)
    else:
        for f in dir_list:
            local_file = f'{CONTAINER_LOG_PATH}{f}'
            try:
                S3.head_object(Bucket=LOG_BUCKET, Key=f)
            except ClientError:
                try:
                    S3.upload_file(local_file, LOG_BUCKET, f)
                except S3UploadFailedError:
                    app.logger.warning(f'文件上传失败: {local_file}')
                    continue
                else:
                    os.remove(local_file)
            else:
                os.remove(local_file)
