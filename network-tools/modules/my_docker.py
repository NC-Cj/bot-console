import contextlib
import os
import time

import docker
from docker import DockerClient
from docker.errors import APIError

IMAGE = os.environ.get("IMAGE")



class MyDocker:

    def __init__(self, docker_url: str):
        self.client = DockerClient(base_url=docker_url)


    def docker_run(self, *args, **kwargs):
        return self.client.containers.run(*args, **kwargs)

    def docker_find_container(self, filters: dict, all_=True, *args, **kwargs):
        """
        查找容器

        Args:
            filters: docker ps --filter {ker: value}
            all_: 默认查找所有容器，docker ps --all

        Returns:
            查找到容器返回容器列表，没有返回 False
        """
        try:
            res = self.client.containers.list(all_, filters=filters, *args, **kwargs)
            return False if res is None or not res else res
        except docker.errors.NotFound:
            return False

    def docker_run_command(self, container_name, container_flag, command, args, remove=False):
        """
        在 docker 中去执行设备的烧录、写号、定位、其他命令的一个封装 API

        Args:
            container_name (str): 容器名称
            container_flag (str): 容器 `label` 标签
            command (str): 执行的动作，详见 object: By
            args (dict): 传给指令的占位符映射表，是一个字典类型
            remove (bool): 容器结束后，是否自动删除，False: 不会自动删除，True: 自动删除

        Returns:
            如果不是捕获的异常 (容器名称重复)， 它将返回错误的说明信息: e.explanation
            如果一切顺利，他应该返回: False

        """

        try:
            from config import LABEL
            self.docker_run(
                image='busybox' if args.get('time', None) else IMAGE,
                command=command.format_map(args),
                labels={LABEL: container_flag},
                name=container_name,
                detach=True,
                remove=remove
            )
        except APIError as e:
            if not e.explanation.endswith('that container to be able to reuse that name.'):
                return e.explanation
        except Exception as e:
            from modules import app
            app.logger.exception(f'docker_run_command Exception: {e}')
            return e.args

        return False
