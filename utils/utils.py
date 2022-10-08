
import httpx
import os
import ssl

from cord import variables

def get_cookies(proxy):
    headers = {
        "accept": "*/*",
        "user-agent": "Discord-Android/131107;RNA",
        "accept-language": "en-US",
        "accept-encoding": "gzip"
    }
    context = ssl.create_default_context()
    context.minimum_version.TLSv1_3
    client = httpx.Client(http2=True, verify=context, headers=headers, proxies=proxy)
    response = client.get(url="https://discord.com/", timeout=30)
    dcfduid = response.headers['Set-Cookie'].split('__dcfduid=')[1].split(';')[0]
    sdcfduid = response.headers['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0]
    cookie = f'__dcfduid={dcfduid}; __sdcfduid={sdcfduid};'
    return cookie
    

def _update_title():
    os.system(f'title SUG [Joined: {variables.joined} , Failed to join: {variables.failed_join}]')
