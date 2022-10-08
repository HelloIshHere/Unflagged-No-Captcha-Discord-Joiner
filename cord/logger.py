from colorama import Fore, Style
import threading
from datetime import datetime

__lock__ = threading.Lock()
def s_print(message):
    __lock__.acquire()
    print(message, flush=True)
    __lock__.release()


def error(text):
    ts = datetime.now() 
    s_print(f"{Fore.RED}[{Fore.WHITE}ERROR{Fore.RED}]  {Fore.CYAN}[{ts.hour}:{ts.minute}:{ts.second}]{Fore.RED}  {text}")
    
def failed(text):
    ts = datetime.now() 
    s_print(f"{Fore.RED}[{Fore.WHITE}FAILED{Fore.RED}]  {Fore.CYAN}[{ts.hour}:{ts.minute}:{ts.second}]{Fore.RED}  {text}")
    
def warn(text):
    ts = datetime.now()
    s_print(f"{Fore.YELLOW}[{Fore.WHITE}WARN{Fore.YELLOW}]  {Fore.RED}[{ts.hour}:{ts.minute}:{ts.second}]{Fore.YELLOW}  {text}")

def info(text):
    ts = datetime.now() 
    s_print(f"{Fore.CYAN}[{Fore.WHITE}INFO{Fore.CYAN}]  {Fore.GREEN}[{ts.hour}:{ts.minute}:{ts.second}]{Fore.CYAN}  {text}")

def success(text):
    ts = datetime.now() 
    s_print(f"{Fore.GREEN}[{Fore.WHITE}SUCCESS{Fore.GREEN}]  {Fore.MAGENTA}[{ts.hour}:{ts.minute}:{ts.second}]{Fore.GREEN}  {text}")

def _input():
    s = input(f"                {Fore.GREEN}[{Fore.WHITE}>{Fore.GREEN}]{Fore.WHITE} ")
    return s
