import httpx
import utils.headers as uh
import utils.utils as uu
import time
import threading
import ssl
import certifi

from colorama import Fore, Style
from datetime import datetime
from cord import logger
from cord import captcha
from cord import variables

__lock__ = threading.Lock()
def logPrint(message):
    __lock__.acquire()
    print(message, flush=True)
    __lock__.release()

levels = [
    "Verification level is 0",
    "Must have verified email on account",
    "Must be registered on Discord for longer than 5 minutes",
    "Must be a member of the server for longer than 10 minutes",
    "Must have a verified phone number"
]

class Joiner():
    def __init__(self, token, proxy, invite_link, solve_captcha, delayBetweenJoins):
        self.token = token
        self.proxy = proxy
        self.invite_link = invite_link
        self.solve_captcha = solve_captcha
        try:
            self.cookie = uu.get_cookies(self.proxy)
        except Exception as e:
            logger.error(f'Error while loading cookies -> {e}')
            return
        self.join()
        time.sleep(delayBetweenJoins)
        variables.total += 1

    def join(self):

        try:
            headers = uh.joiner_headers(self.token, self.cookie)
            context = ssl.create_default_context()
            context.minimum_version.TLSv1_3
            client = httpx.Client(http2=True, verify=context, proxies=self.proxy, headers=headers)

            req = client.post(f"https://discord.com/api/v9/invites/{self.invite_link}", json={})
            if "The user is banned from this guild" in req.text:
                logger.failed(f'[{self.token}] Is banned from this guild')
                variables.failed_join += 1
                return

            elif "Maximum number of guilds reached (100)" in req.text:
                error = req.text
                logger.failed(f'[{self.token}] Token has reached the maximum number of guilds')
                variables.failed_join += 1
                uu._update_title()
                return

            elif "You need to verify your account in order to perform this action" in req.text:
                ts = datetime.now()
                error = req.text
                logger.failed(f'[{self.token}] Token Is Locked, Make sure to use unlocked tokens.')
                variables.failed_join += 1
                uu._update_title()
                return
                
            if req.status_code == 200:
                variables.joined += 1
                uu._update_title()
                json = req.json()
                guild = json["guild"]
                id = guild["id"]
                name = guild["name"]
                verification_level = guild["verification_level"]
                ts = datetime.now() 
                logger.success(f'[{self.token}] Joined {name} -> [{ levels[int(verification_level)] }]')
                if "show_verification_form" in req.text:
                    show_verification_form = json["show_verification_form"]
                    if show_verification_form == True or show_verification_form == "true":
                        self.bypass(id, name, self.invite_link, self.token)
                return
                
            
            elif req.status_code == 401:
                ts = datetime.now() 
                error = req.text
                logger.failed(f'[{self.token}] Token is invalid please make sure tokens are valid: {error}')
                variables.failed_join += 1
                uu._update_title()
                return

            elif req.status_code == 403 and "You need to verify your account in order to perform this action" in req.text:
                error = req.text
                logger.failed(f'[{self.token}] Token Is Locked, Make sure to use unlocked tokens.')
                variables.failed_join += 1
                uu._update_title()
                return
                
            elif req.status_code == 429:
                error = req.text
                logger.error(f'[{self.token}] Please make sure to use proxies, your IP being rate limited')
                variables.failed_join += 1
                uu._update_title()
                return

            elif req.status_code == 400:
                if self.solve_captcha == True:
                    if "captcha_key" in req.text:
                        ts = datetime.now() 
                        logPrint(f"{Fore.RED}[{Fore.WHITE}WARN{Fore.RED}]{Fore.WHITE} - {Fore.RED}[{Fore.WHITE}{self.token[:40]}***{Fore.RED}]{Fore.WHITE} - Captcha found | Solving = {self.solve_captcha}{Fore.RESET}")
                        site_key = req.json()["captcha_sitekey"]
                        if "captcha_rqdata" in req.text:
                            rqdata = req.json()["captcha_rqdata"]
                            rqtoken = req.json()["captcha_rqtoken"]
                            cap = captcha.Solver(rqdata, site_key, 'https://discord.com/', self.proxy)
                            _cap = cap.solve()
                            if _cap == False:
                                logger.error('Unsupported captcha API') # unsupported
                                return
                            req2 = client.post(f"https://discord.com/api/v9/invites/{self.invite_link}", json={"captcha_key": _cap, "captcha_rqtoken": rqtoken})
                        else:
                            cap = captcha.Solver(None, site_key, self.proxy)
                            _cap = cap.solve()
                            if _cap == False:
                                logger.error('Unsupported captcha API') # unsupported
                                return
                            req2 = client.post(f"https://discord.com/api/v9/invites/{self.invite_link}", json={"captcha_key": _cap})#, "captcha_rqtoken": rqtoken})
                        if req2.status_code == 200:
                            variables.joined += 1
                            uu._update_title()
                            json = req2.json()
                            guild = json["guild"]
                            id = guild["id"]
                            name = guild["name"]
                            verification_level = guild["verification_level"]

                            logger.success(f'[{self.token}] Joined {name} -> [{ levels[int(verification_level)] }]')
                            if "show_verification_form" in req2.text:
                                show_verification_form = json["show_verification_form"]
                                if show_verification_form == True or show_verification_form == "true":
                                    self.bypass(id, name, self.invite_link, self.token)
                            
                        elif req2.status_code == 403 and "You need to verify your account in order to perform this action" in req2.text:
                            error = req2.text
                            logger.failed(f'[{self.token}] Token Is Locked, Make sure to use unlocked tokens.')
                            variables.failed_join += 1
                            uu._update_title()
                            return
                        elif req2.status_code == 429:
                            error = req2.text
                            logger.error(f'[{self.token}] Please make sure to use proxies, your IP being rate limited')
                            variables.failed_join += 1
                            uu._update_title()
                            return
                else:
                    variables.failed_join += 1
                    variables.join_captcha += 1
                    uu._update_title()
                    j = req.text
                    time.sleep(0.01)
                    logger.warn(f'[{self.token}] - Captcha found | Solving = {self.solve_captcha}{Fore.RESET}')
                    return
            else:
                j = req.text
                logPrint(f"unknown error message while joining the server -> [{j}] ({req.status_code})")

        except Exception as e:
            ts = datetime.now() 
            print(f"[{Fore.RED}ERROR{Style.RESET_ALL}]{Fore.CYAN} - {Fore.RED}Exception: {e}{Style.RESET_ALL}")
        
            
    def bypass(self, id, name, invite_link, token):
        new_headers1 = uh.bypass_headers(type="1", token=token, cookie=self.cookie)
        new_headers2 = uh.bypass_headers(type="2", token=token, cookie=self.cookie)

        self.bypassURL1 = f'https://discord.com/api/v9/guilds/{id}/member-verification?with_guild=false&invite_code={invite_link}'
        self.bypassURL2 = f'https://discord.com/api/v9/guilds/{id}/requests/@me'

        context = ssl.create_default_context()
        context.minimum_version.TLSv1_3
        client = httpx.Client(http2=True, verify=context, proxies=self.proxy, headers=new_headers1)

        context = httpx.create_ssl_context()
        context.load_verify_locations(cafile=certifi.where())
        context.set_alpn_protocols(["h2"])
        context.minimum_version.MAXIMUM_SUPPORTED
        CIPHERS = 'ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES'
        context.set_ciphers(CIPHERS)
        client2 = httpx.Client(http2=True, verify=context, proxies=self.proxy, headers=new_headers2)

        try:
            rq1 = client.get(self.bypassURL1) 
            if rq1.status_code == 200 or 201:
                pass
            if "The user is banned from this guild" in rq1.text:
                error = rq1.text
                logger.failed(f'[{self.token}] Is banned from this guild')
                variables.failed_join += 1
                return
            if rq1.status_code == 400:
                error = rq1.text
                logger.error(f'{self.token} Error while bypassing verification screen: {error}')
                variables.failed_join += 1
                return
            elif rq1.status_code == 403:
                error = rq1.text
                logger.failed(f'[{self.token}] Failed to bypass verification screen: {error}')
                variables.failed_join += 1
                return
            elif rq1.status_code == 200:
                json = rq1.json()
                rq2 = client2.put(self.bypassURL2, json=json)
                if rq2.status_code == 200 or 201:
                    logger.success(f"Succesfully bypassed verification screen -> ({self.token}) - Server: {name}")
                    return
                elif rq2.status_code == 400:
                    error = rq2.text
                    logger.error(f'{self.token} Error while bypassing verification screen: {error}')
                    variables.failed_join += 1
                    return
                elif rq2.status_code == 403: 
                    error = rq2.text
                    logger.failed(f'[{self.token}] Failed to bypass verification screen: {error}')
                    variables.failed_join += 1
                    return
                else:
                    error = rq2.text
                    logger.error(f'[{self.token}] Error While bypassing verification screen: {error}')
                    variables.failed_join += 1
                    return
            else:
                error = rq1.text
                logger.error(f'[{self.token}] Error While bypassing verification screen: {error}')
                variables.failed_join += 1
                return
        except Exception as e:
            print(f'Exception: {e}')