import re
from datetime import datetime

from Data import config

from extras import SendDiscord
#from extras import ForwardTelegram


from bs4 import BeautifulSoup as bs
from colorama import Fore, init

init(autoreset = True)

def get_current_time():

    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log(text):

    _file = open('logs.txt', 'a', encoding='utf-8')
    _file.write(f"[{get_current_time()}] {str(text)}\n")


def write_wfp(text, _type, _log):

    msg = f'{Fore.LIGHTMAGENTA_EX}[{get_current_time()}]{Fore.YELLOW} - '

    if _type == 'info':

        msg += f'{Fore.LIGHTCYAN_EX}{text}'

    elif _type == 'danger':

        msg += f'{Fore.RED}{text}'

    elif _type == 'success':

        msg += f'{Fore.LIGHTGREEN_EX}{text}'
    
    elif _type == 'plain':

        msg += f'{Fore.WHITE}{text}'
    
    elif _type == 'custom':

        msg += f'{text}'


    print(msg)

    if _log == True:

        log(text)


def Parser(text):

    urls = []

    for word in text.split(' '):


        if any(any(s in word for s in subList) for subList in config.domains.values()):
        # if any(_ in word for _ in config.domains) == True:
            
            urls.append(
                
                re.findall(
                    
                    'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/(?:[-\w.]|(?:%[\da-fA-F]{2}))+',
                    word
                
                )
                [0]
            )
    
    return urls

#Parser("alıon porosdf https")


def PndTlReqs(soup, ad_form_data):

    try:

        csrf = soup.find(
            
            'input',
            attrs = {

                "name": "_csrfToken"

            }
        
        )['value']
    
    except: csrf = "damn"            
    
    try:

        tkn = soup.find(

            'input',
            attrs = {

                "name": "tkn"

            }

        )['value']
    
    except: tkn = "damn"
    
    try:

        TokenFields = soup.find(
            
            "input",
            attrs = {
                
                "name": "_Token[fields]"
            
            }
        )["value"]
    
    except: TokenFields = "damn"

    try:

        TokenUnlocked = soup.find(
            
            "input",
            attrs = {
                
                "name": "_Token[unlocked]"
            
            }
        
        )["value"]
    
    except: TokenUnlocked = "damn"

    if ad_form_data == False:
        
        return csrf, tkn, TokenFields, TokenUnlocked
    
    else:

        try:

            AdFormData = soup.find(

                "input",
                attrs = {

                    "name": "ad_form_data"

                }

            )['value']
        
        except: AdFormData = "damn"

        return csrf, tkn, TokenFields, TokenUnlocked, AdFormData


def SaveTxt(Name, ShortUrl, FinishUrl, link = False):

    txt = f"[{get_current_time()}] {Name} kanalına atılan"
    
    if link != False:
    
        txt += f" ({link})"
    
    txt += f" {ShortUrl} linkini geçtim: {FinishUrl}\n"

    open("linkler.txt", "a", encoding="utf-8").write(txt)


def Sender(Name, ShortUrl, FinishUrl, Message, MessageID, ChannelID, link = False):

    if config.send_to['discord']['status']:
   
        SendDiscord.Send(Name, Message, ShortUrl, FinishUrl, link)

    # if config.send_to['telegram']['status']:

    #     pass
       
    # if config.send_to['telegram']['Forward']['status']:

    #     ForwardTelegram.Forward(ChannelID, MessageID)