from flask import make_response, send_file, jsonify

from config import CONTAINER_LOG_PATH, docker_
from modules import app
from modules.tools import post_params, get_s3_logs, update_source, to_format
from pages.log import log_blue


@log_blue.route('/showLogs', methods=['POST'])
def show_logs():
    mac = post_params("mac")
    name = to_format(mac)

    containers = docker_.docker_find_container({"name": name})
    if containers is False:
        source = update_source({"code": -1, "msg": "该mac地址容器未找到"})
    else:
        _, status = docker_.get_docker_container_status(containers)
        logs = docker_.get_docker_container_logs(containers)
        read_state = 1 if status == "running" else 0
        source = update_source({"msg": logs, "read_state": read_state})

    return jsonify(source)
