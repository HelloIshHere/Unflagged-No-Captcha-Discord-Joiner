from cord import joiner, logger, variables
import random, json, threading, sys, time, os
from colorama import Fore

def exit():
    logger.error("Press enter to exit...")
    input("\n\n")
    sys.exit()

def loadConfig():
    try:
        with open("config.json") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(e)
        return False

def loadTokens():
    try:
        tokens = []
        with open("input/tokens.txt") as f:
            for line in f:
                token = line.replace("\n", "")
                if ":" in token:
                    token = token.split(":")[2]
                tokens.append(token)
        return tokens
    except Exception as e:
        print(e)
        return False

def loadProxies():
    try:
        proxies = []
        with open("input/proxies.txt") as f:
            for line in f:
                proxies.append(line.replace("\n",""))
        return proxies
    except Exception as e:
        print(e)
        return False

def loadInvites():
    try:
        invites = []
        with open("input/invites.txt") as f:
            for line in f:
                if ".gg/" in line:
                    inviteCode = line.split(".gg/")[1]
                elif ".com/" in line:
                    inviteCode = line.split(".com/")[1]
                else:
                    inviteCode = line
                invites.append(inviteCode)
        return invites
    except Exception as e:
        print(e)
        return False

def main():
    try:
        # Reseting variables
        variables.failed_join = 0
        variables.join_captcha = 0
        variables.total = 0
        variables.joined = 0

        # loading config and tokens and proxies
        config = loadConfig()
        tokens = loadTokens()
        proxies = loadProxies()
        invites = loadInvites()

        # Checking for errors from loading
        if config == False:
            exit()
        if tokens == False:
            exit()
        if proxies == False:
            exit()
        if invites == False:
            exit()

        # Threads to run
        threads = int(input(f"                {Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} How many threads to run (0 = Maximum): "))
        if threads == 0:
            threads = len(tokens)
        elif threads > len(tokens):
            threads = len(tokens)

        delayBetweenJoins = int(input(f"                {Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} Enter delay between joins: "))


        if invites == []:
            inviteLink = input(f"                {Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} No invite links found in input/invites.txt enter an invite link: ")
            if ".gg/" in inviteLink:
                inviteCode = inviteLink.split(".gg/")[1]
            elif ".com/" in inviteLink:
                inviteCode = inviteLink.split(".com/")[1]
            else:
                inviteCode = inviteLink

        if invites != []:
            for invite in invites:
                for token in tokens:
                    while threading.active_count() >= threads:
                        if threads == 1:
                            threads += 1
                        time.sleep(0.1)
                    proxy = 'https://' + random.choice(proxies) if len(proxies) > 0 else None
                    thread = threading.Thread(target=joiner.Joiner, args=(token, proxy, invite, config["captcha_settings"]["solve_captchas"], delayBetweenJoins,))
                    thread.start()

            while True:
                if variables.total >= len(tokens):
                    time.sleep(3)
                    finishText = f'''
    {Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} Finished Joining


    {Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}]{Fore.WHITE} Joined: {variables.joined}
    {Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}]{Fore.WHITE} Failed: {variables.failed_join}
    {Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}]{Fore.WHITE} Captchas: {variables.join_captcha}
            '''
                    print(finishText)
                    input('Press enter to return\n\n')
                    main()
                    break
        else:
            for token in tokens:
                while threading.active_count() >= threads:
                    if threads == 1:
                        threads += 1
                    time.sleep(0.1)
                proxy = 'https://' + random.choice(proxies) if len(proxies) > 0 else None
                thread = threading.Thread(target=joiner.Joiner, args=(token, proxy, inviteCode, config["captcha_settings"]["solve_captchas"], delayBetweenJoins,))
                thread.start()

        while True:
            if variables.total >= len(tokens):
                time.sleep(3)
                finishText = f'''
    {Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} Finished Joining


    {Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}]{Fore.WHITE} Joined: {variables.joined}
    {Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}]{Fore.WHITE} Failed: {variables.failed_join}
    {Fore.GREEN}[{Fore.WHITE}*{Fore.GREEN}]{Fore.WHITE} Captchas: {variables.join_captcha}
        '''
                print(finishText)
                input('Press enter to return\n\n')
                main()
                break
    except Exception as e:
        logger.error(e)

if __name__ == "__main__": 
    os.system("cls")
    main()