import yaml


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner


@singleton
class HttpClientConfig:

    def __init__(self):
        config_path = './app/config/ServerConfig.yaml'
        config = yaml.load(open(config_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)
        self.host = config["server"]["host"]
        self.port = config["server"]["port"]
        self.timeout = config["server"]["timeout"]


adminConfig = HttpClientConfig()

# class HttpClientUtils:
#
#     @staticmethod
#     async def doPost(url,
#                      params=None,
#                      headers=None,
#                      files=None,
#                      json=None, ):
#         async with httpx.AsyncClient() as client:
#             client.post()
#             pass
#
#     @staticmethod
#     async def doGet(url,
#                     params=None,
#                     headers=None,
#                     files=None,
#                     json=None, ):
#         async with httpx.AsyncClient() as client:
#             client.get()
#             pass
#
#     @staticmethod
#     async def doPut(url, header, params):
#         pass
