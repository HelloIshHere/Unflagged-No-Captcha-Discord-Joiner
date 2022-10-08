import httpx
import json
from cord import logger
import time
import twocaptcha
from cord import variables

with open("config.json") as f:
    config = json.load(f)

captcha_api = config["captcha_settings"]["captcha_api"]
captcha_api_key = config["captcha_settings"]["captcha_api_key"]
captcha_timeout = 120

class Solver():
    def __init__(self, rqdata, site_key, url, proxy):
        self.url = url
        self.rqdata = rqdata
        self.site_key = site_key
        self.proxy = proxy

    def solve(self):
        if captcha_api == "2captcha.com":
            c = self._2captcha()
            return c
        elif captcha_api == "anti-captcha.com" or captcha_api == "capmonster.cloud" or captcha_api == "anycaptcha.com":
            c = self.anti_monster()
            return c
        else:
            return False # unsupported

    def _2captcha(self):
        #variables.runningCaptchaTasks += 1
        data = {}
        if self.rqdata != None:
            data = {
                "userAgent": "Discord-Android/131107;RNA",
                "data": self.rqdata
            }
        else:
            data = {
                "user-agent": "Discord-Android/131107;RNA"
            }   
        cap = twocaptcha.TwoCaptcha(captcha_api_key).hcaptcha(sitekey=self.site_key, url=self.url, param1=data)
        j = cap["code"]
        #variables.solvedCaptchas += 1
        #variables.runningCaptchaTasks -= 1
        return j

    def anti_monster(self):
        #variables.runningCaptchaTasks += 1
        client = httpx.Client(proxies=self.proxy)

        solvedCaptcha = None
        payload = {}
        if self.rqdata != None:
            payload = {
                "clientKey": captcha_api_key, 
                "task": {
                    "type": "HCaptchaTaskProxyless", "websiteURL": self.url,
                    "websiteKey": self.site_key,
                    "userAgent": "Discord-Android/131107;RNA",
                    "enterprisePayload": {
                        "rqdata": self.rqdata,
                        "sentry": True
                    }
                }
            }
        else:
            payload = {
                "clientKey": captcha_api_key, 
                "task": {
                    "type": "HCaptchaTaskProxyless", "websiteURL": self.url,
                    "websiteKey": self.site_key,
                    "userAgent": "Discord-Android/131107;RNA"
                }
            }
        taskId = ""
        taskId = client.post(f"https://api.{captcha_api}/createTask", json=payload, timeout=captcha_timeout).json()
        if taskId.get("errorId") > 0:
            #print(f"createTask - {taskId.get('errorDescription')}")
            return None
        taskId = taskId.get("taskId")

        while not solvedCaptcha:
            captchaData = client.post(f"https://api.{captcha_api}/getTaskResult", json={"clientKey": captcha_api_key, "taskId": taskId}, timeout=captcha_timeout).json()
            if captchaData.get("status") == "ready":
                #variables.solvedCaptchas += 1
                solvedCaptcha = captchaData.get(
                    "solution").get("gRecaptchaResponse")
                #variables.runningCaptchaTasks -= 1
                return solvedCaptcha