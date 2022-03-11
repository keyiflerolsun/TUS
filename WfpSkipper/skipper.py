import re
import time

from WfpSkipper import utils

import requests
from bs4 import BeautifulSoup as bs


class UrlSkipper():

    def __init__(self) -> None:
        
        self.TrLinkTokenUrl     = "https://aylink.co/get/tk"
        self.TrLinkSkipUrl      = "https://aylink.co/links/go2"
        
        self.PndTlSkipUrl       = "https://pnd.one/links/go"

        self.OuoSkipUrl         = "https://ouo.io/xreallcygo"

    def TrLink(self, url):

        code = url.split('/')[3]
        domain = url.split('/')[2]

        headers = {
            
            "Sec-Ch-Ua"                     : "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"98\"",
            "Sec-Ch-Ua-Mobile"              : "?0",
            "Sec-Ch-Ua-Platform"            : "\"Windows\"",
            "Upgrade-Insecure-Requests"     : "1",
            "User-Agent"                    : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
            "Accept"                        : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site"                : "none",
            "Sec-Fetch-Mode"                : "navigate",
            "Sec-Fetch-User"                : "?1",
            "Sec-Fetch-Dest"                : "document",
            "Accept-Encoding"               : "gzip, deflate",
            "Accept-Language"               : "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection"                    : "close"
        
        }
        
        r = requests.get(
            
            url,
            headers = headers
        
        )

        #r.cookies -> ['bck', 'dm', 'lang', 'online', 'visitor']

        soup = bs(r.text, 'html.parser')

        try:

            csrf = soup.find(
                
                'input',
                attrs = {

                    "name": "csrf"

                }
            
            )['value']
        
        except:

            csrf = "damn"

        _a = re.findall('let _a = \'(.*)\',', r.text)
        _t = re.findall('_t = \'(.*)\',', r.text)
        _d = re.findall('_d = \'(.*)\';', r.text)
        
        if any(vrbl == [] for vrbl in [_a, _t, _d]):

            tkn = False
        
        else:
            
            tkn = True
            cookies = r.cookies

            # cookies['_ym_isad'] = "2"
            # cookies['_ym_visorc'] = "b"
            # cookies['wndpn'] = "1"

            headers['Content-Type']         = "application/x-www-form-urlencoded; charset=UTF-8"
            headers['X-Requested-With']     = "XMLHttpRequest"
            headers['Origin']               = f"https://{domain}"
            headers['Referer']              = f"https://{domain}/{code}"

            data = {
                
                "_a": _a,
                "_t": _t,
                "_d": _d
            
            }

            rr = requests.post(
                
                self.TrLinkTokenUrl,
                headers=headers,
                cookies=cookies,
                data=data
            
            )

            try:

                json_rsp = rr.json()
                
                token = json_rsp['th'] if json_rsp['status'] else 'damn'

            except:
                token = "damn"

                tkn = False
        
        headers['Sec-Fetch-Mode'] = "cors"

        data = {}
        data['alias'] = code
        
        if csrf != 'damn':

            data['csrf'] = token
        
        
        if token != 'damn':

            data['token'] = token
        
        # print(rr.text)

        try:
            
            cookies['TRLink'] = rr.cookies.get_dict['TRLink']

        except:

            pass
    
        rrr = requests.post(
            
            self.TrLinkSkipUrl,
            headers           = headers,
            data              = data,
            allow_redirects   = False,
            cookies           = cookies # Otomatik olarak son linki verecektir eğer bu özellik kalkar ise yorum satırını devre dışı bırakın
        
        )

        try:

            json_response = rrr.json()
            
            if json_response['url'].split('/')[2] != 'bildirim.eu':
                
                return json_response['url']
            
            else:
                
                GoBildirim = requests.get(json_response['url'])
                url_data = re.findall("url = '((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", str(GoBildirim.text))
                url = url_data[0][0]

                return url

        except:

            pass
    
    def PndTl(self, url):

        code = url.split('/')[3]
        domain = url.split('/')[2]

        headers = {
            
            "Sec-Ch-Ua"                     : "\"(Not(A:Brand\";v=\"8\", \"Chromium\";v=\"98\"",
            "Sec-Ch-Ua-Mobile"              : "?0",
            "Sec-Ch-Ua-Platform"            : "\"Windows\"",
            "Upgrade-Insecure-Requests"     : "1",
            "Pragma"                        : "no-cache",
            "User-Agent"                    : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
            "Accept"                        : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site"                : "none",
            "Sec-Fetch-Mode"                : "navigate",
            "Sec-Fetch-User"                : "?1",
            "Sec-Fetch-Dest"                : "document",
            "Accept-Encoding"               : "gzip, deflate",
            "Accept-Language"               : "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control"                 : "no-cache",
            "Connection"                    : "close"
        
        }

        r = requests.get(
            
            url,
            headers = headers
        
        )

        soup = bs(r.text, "html.parser")

        ####################################
        
        csrf, tkn, TokenFields, TokenUnlocked = utils.PndTlReqs(soup, False)

        ####################################

        if any(vrbl == "damn" for vrbl in [csrf, tkn, TokenFields, TokenUnlocked]):

            return "damn"

        else:


            data = {

                "_method"           : "POST",
                "_csrfToken"        : csrf,
                "ref"               : "",
                "f_n"               : "slc",
                "tkn"               : tkn,
                "_Token[fields]"    : TokenFields,
                "_Token[unlocked]"  : TokenUnlocked 

            }

            headers['Origin'] = f"https://{domain}"
            headers['Content-Type'] = "application/x-www-form-urlencoded"

            rr = requests.post(
                
                url,
                headers = headers,
                data = data,
                cookies = r.cookies.get_dict()
            
            )

            soup = bs(rr.text, "html.parser")

            csrf, tkn, TokenFields, TokenUnlocked, AdFormData = utils.PndTlReqs(soup, True)

            data = {
            
                "_method"               : "POST",
                "_csrfToken"            : csrf,
                "ad_form_data"          : AdFormData,
                "_Token[fields]"        : TokenFields,
                "_Token[unlocked]"      : TokenUnlocked
            
            }

            headers['Referer']              = url
            headers['Sec-Fetch-Dest']       = "empty"
            headers['X-Requested-With']     = "XMLHttpRequest"
            

            cookies = {
             
                "lang"              : "en-US",
                "AppSession"        : r.cookies.get_dict()["AppSession"],
                "csrfToken"         : r.cookies.get_dict()["csrfToken"],
                "app_visitor"       : rr.cookies.get_dict()["app_visitor"],
                "pndclkid"          : r.cookies.get_dict()["pndclkid"],
                "ab"                : "2"
            
            }

            time.sleep(15)


            rrr = requests.post(
                
                f"https://{domain}/links/go",
                #self.PndTlSkipUrl,
                headers     = headers,
                cookies     = cookies,
                data        = data
            
            
            )

            json_resp = rrr.json()

            if 'status' in json_resp.keys():

                if json_resp['status'] == "success":

                    return json_resp['url']
                
                else:
            
                    return "damn"
            
            else:

                return "damn"

    def Ouo(self, url):

        code = url.split('/')[3]
        domain = url.split('/')[2]

        headers = {
            
            "Connection"                    : "close",
            "Upgrade-Insecure-Requests"     : "1",
            "User-Agent"                    : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
            "Accept"                        : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site"                : "none",
            "Sec-Fetch-Mode"                : "navigate",
            "Sec-Fetch-Dest"                : "document",
            "Accept-Encoding"               : "gzip, deflate",
            "Accept-Language"               : "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"

        }

        r = requests.get(
            
            url,
            headers = headers
        
        )

        soup = bs(r.text, "html.parser")

        try:

            token = soup.find(
                
                'input',
                attrs = {

                    "name": "_token"

                }
            
            )['value']
        
        except:

            token = "damn"
        

        

        
        headers['Cache-Control']    = "max-age=0"
        headers['Sec-Fetch-Site']   = "same-origin"
        headers['Origin']           = f"https://{domain}"
        headers['Referer']          = f"https://{domain}/go/{code}"

        data = {
     
            "_token": token
        }

        rr = requests.post(
            
            f"{self.OuoSkipUrl}/{code}",
            headers             = headers,
            cookies             = r.cookies.get_dict(),
            data                = data,
            allow_redirects     = False

        )

        soup = bs(rr.text, 'html.parser')
        url = soup.find('a').attrs['href']
        
        return url
