import httpx
import requests
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
        self.client_config = "./app/config/ClientConfig.yaml"
        self.token = ""
        self.refresh_token = ""

    def setToken(self, token: str):
        self.token = token

    def setRefreshToken(self, token: str):
        self.refresh_token = token


adminConfig = HttpClientConfig()


class HttpClientUtils:
    refreshUrl = f"http://{adminConfig.host}:{adminConfig.port}/admin/usr/refresh/token"

    def __init__(self):
        pass

    @staticmethod
    def doPostWithToken(url, params=None, data=None, headers=None, files=None):
        # * 附带token的POST请求
        # * 若token过期，自动使用refreshToken请求刷新
        # * 若refreshToken过期，抛出HTTPStatusError
        if headers is None:
            headers = {}
        headers["token"] = adminConfig.token
        client = httpx.Client()
        try:
            response = client.post(url, params=params, data=data, headers=headers, files=files)
            # token过期，使用refreshToken刷新
            if response.status_code == 401:
                re = client.post(HttpClientUtils.refreshUrl, data={"refreshToken": adminConfig.refresh_token})
                # ! refreshToken过期，抛出异常
                if re.status_code == 401:
                    re.raise_for_status()
                # *修改token和refreshToken
                adminConfig.setToken(re.json()["token"])
                adminConfig.setRefreshToken(re.json()["refreshToken"])
                # *重新执行请求
                response = client.post(url, params=params, data=data, headers=headers)
                return response
        except Exception as e:
            raise e

    @staticmethod
    def doGetWithToken(url, params={}, headers=None):
        # * 附带token的GET请求
        # * 若token过期，自动使用refreshToken请求刷新
        # * 若refreshToken过期，抛出HTTPStatusError
        if headers is None:
            headers = {}
        headers["token"] = adminConfig.token
        client = httpx.Client()
        try:
            response = client.get(url, params=params, headers=headers)
            if response.status_code == 401:
                re = client.post(HttpClientUtils.refreshUrl,
                                 json={"token": adminConfig.token,
                                       "refreshToken": adminConfig.refresh_token})
                # ! refreshToken过期，抛出异常
                if re.status_code == 401:
                    re.raise_for_status()
                # *修改token和refreshToken
                adminConfig.setToken(re.json()["data"]["token"])
                adminConfig.setRefreshToken(re.json()["data"]["refreshToken"])
                # *重新执行请求
                headers["token"] = adminConfig.token
                response = client.get(url, params=params, headers=headers)
                return response
        except Exception as e:
            print(e)
            raise e
        return response

    @staticmethod
    async def doPost(url,
                     params=None,
                     headers=None,
                     files=None,
                     json=None, ):
        async with httpx.AsyncClient() as client:
            await client.post(url)
            pass

    @staticmethod
    async def doGet(url,
                    params=None,
                    headers=None,
                    files=None,
                    json=None, ):
        async with httpx.AsyncClient() as client:
            client.get()
            pass

    @staticmethod
    async def doPut(url, params=None, headers=None, files=None, json=None, ):
        pass

    @staticmethod
    def doPutWithToken(url, params=None, headers=None, files=None, data=None):
        pass
