

def cookie_headers():
    return {
        "accept": "*/*",
        "user-agent": "Discord-Android/131107;RNA",
        "accept-language": "en-US",
        "accept-encoding": "gzip"
    }


def joiner_headers(token, cookie, type="2"):
    pc_headers = { # patched headers
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Alt-Used': 'discord.com',
        'Authorization': token,
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/json',
        'Cookie': cookie,
        'Host': 'discord.com',
        'Origin': 'https://discord.com',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijk5Njg1OTI5NzU3MTAyOTA2MiIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5OTY4NTk3NDEyMjM1MjI0ODUiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9',
        'X-Debug-Options': 'bugReporterEnabled',
        'X-Discord-Locale': 'en-US',
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6Imh0dHBzOi8vd3d3Lmdvb2dsZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6Ind3dy5nb29nbGUuY29tIiwic2VhcmNoX2VuZ2luZSI6Imdvb2dsZSIsInJlZmVycmVyX2N1cnJlbnQiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6Ind3dy5nb29nbGUuY29tIiwic2VhcmNoX2VuZ2luZV9jdXJyZW50IjoiZ29vZ2xlIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM4MjU0LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
    }

    mobile_headers = { # fixed
        'accept-encoding': 'gzip',
        'accept-language': 'en-US',
        'authorization': token,
        'connection': 'Keep-Alive',
        'content-type': 'application/json',
        'cookie': cookie,
        'host': 'discord.com',
        'user-agent': 'Discord-Android/131107;RNA',
        'x-context-properties': "eyJsb2NhdGlvbiI6IkFjY2VwdCBJbnZpdGUgUGFnZSJ9",
        'x-discord-locale': 'en-US',
        'x-debug-options': 'bugReporterEnabled',
        'x-super-properties': "eyJvcyI6IkFuZHJvaWQiLCJicm93c2VyIjoiRGlzY29yZCBBbmRyb2lkIiwiZGV2aWNlIjoiQW5kcm9pZCBTREsgYnVpbHQgZm9yIHg4Niwgc2RrX3Bob25lX3g4NiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImNsaWVudF92ZXJzaW9uIjoiMTMxLjcgLSBybiIsInJlbGVhc2VfY2hhbm5lbCI6ImJldGFSZWxlYXNlIiwiZGV2aWNlX3ZlbmRvcl9pZCI6IjRiODY0NmU5LTMzMmMtNDhlZS04M2FlLWY4OGU2NmYxYjllMiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6IiIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIzMCIsImNsaWVudF9idWlsZF9udW1iZXIiOjEzMTEwNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
    }

    if type == "2":
        headers = mobile_headers
    else:
        headers = pc_headers
    return headers

def bypass_headers(type=None, token=None, cookie=None):
    if type == "1":
        headers = {
            "accept-encoding": "gzip",
            "accept-language": "en-US",
            "authorization": token,
            "content-type": "application/json",
            "connection": "Keep-Alive",
            "cookie": cookie,
            "host": "discord.com",
            "user-agent": "Discord-Android/131107;RNA",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IkFuZHJvaWQiLCJicm93c2VyIjoiRGlzY29yZCBBbmRyb2lkIiwiZGV2aWNlIjoiQW5kcm9pZCBTREsgYnVpbHQgZm9yIHg4Niwgc2RrX3Bob25lX3g4NiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImNsaWVudF92ZXJzaW9uIjoiMTMxLjcgLSBybiIsInJlbGVhc2VfY2hhbm5lbCI6ImJldGFSZWxlYXNlIiwiZGV2aWNlX3ZlbmRvcl9pZCI6IjRiODY0NmU5LTMzMmMtNDhlZS04M2FlLWY4OGU2NmYxYjllMiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6IiIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIzMCIsImNsaWVudF9idWlsZF9udW1iZXIiOjEzMTEwNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
    elif type == "2":
        headers = {
            "accept-encoding": "gzip",
            "accept-language": "en-US",
            "authorization": token,
            "connection": "Keep-Alive",
            "cookie": cookie,
            "host": "discord.com",
            "user-agent": "Discord-Android/131107;RNA",
            "x-discord-locale": "en-US",
            "x-super-properties": "eyJvcyI6IkFuZHJvaWQiLCJicm93c2VyIjoiRGlzY29yZCBBbmRyb2lkIiwiZGV2aWNlIjoiQW5kcm9pZCBTREsgYnVpbHQgZm9yIHg4Niwgc2RrX3Bob25lX3g4NiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImNsaWVudF92ZXJzaW9uIjoiMTMxLjcgLSBybiIsInJlbGVhc2VfY2hhbm5lbCI6ImJldGFSZWxlYXNlIiwiZGV2aWNlX3ZlbmRvcl9pZCI6IjRiODY0NmU5LTMzMmMtNDhlZS04M2FlLWY4OGU2NmYxYjllMiIsImJyb3dzZXJfdXNlcl9hZ2VudCI6IiIsImJyb3dzZXJfdmVyc2lvbiI6IiIsIm9zX3ZlcnNpb24iOiIzMCIsImNsaWVudF9idWlsZF9udW1iZXIiOjEzMTEwNywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
    return headers