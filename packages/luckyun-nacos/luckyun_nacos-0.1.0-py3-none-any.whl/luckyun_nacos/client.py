import nacos
import asyncio
import threading
import yaml

class Client():
    def __init__(self, server_addresses, service_name=None, service_ip=None, service_port: int = None, heartbeat_rate = 15, endpoint=None, namespace=None, ak=None, sk=None, username=None, password=None):

        self.service_name = service_name
        self.service_ip = service_ip
        self.service_port = service_port
        self.heartbeat_rate = heartbeat_rate

        self.client = nacos.NacosClient(
            server_addresses=server_addresses,
            endpoint=endpoint,
            namespace=namespace,
            ak=ak,
            sk=sk,
            username=username,
            password=password,
        )

    def add_instance(self):
        self.client.add_naming_instance(
            self.service_name, self.service_ip, self.service_port)

        # Create a new thread for the event loop
        self.thread = threading.Thread(target=self.run_event_loop)
        self.thread.start()

    async def remove_instance(self):
        self.client.remove_naming_instance(
            self.service_name, self.service_ip, self.service_port)

    async def task_nacos_heartbeat(self):
        while True:
            await asyncio.sleep(self.heartbeat_rate)
            print("send_heartbeat")
            self.client.send_heartbeat(
                self.service_name, self.service_ip, self.service_port)

    async def run_nacos_heartbeat(self):
        task = asyncio.create_task(self.task_nacos_heartbeat())
        await task

    def run_event_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_nacos_heartbeat())
        self.loop.close()

    def get_config(self, data_id, group="DEFAULT_GROUP"):
        return yaml.load(self.client.get_config(data_id, group), Loader=yaml.FullLoader)
