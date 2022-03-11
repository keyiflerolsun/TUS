from Data import config
from WfpSkipper import utils
from WfpSkipper import skipper

from pyrogram import Client, filters
from colorama import Fore, init

init(autoreset = True)


app = Client("Sessions/WarForPeace", config.TGApiId, config.TGApiHash)


Skipper = skipper.UrlSkipper()

@app.on_message()
async def masum(client, message):
    
    if str(message.chat.id) in config.TGChannels:

        channel = message.chat.title
        
        if message.text != None:

            msg = message.text
        
        if message.caption != None:

            msg = message.caption
        
        else:
            
            return
        
        try:

            link = message.link 
        
        except: link = False
        
        # msg = message.text if not None else message.caption
        
        #print(msg)

        try:

            urls = utils.Parser(msg)

            if urls == []:

                pass

            else:

                resp = "damn"
            #    print(urls)
                for url in urls:

                    if url.split('/')[2] in config.domains['trlink']:
                        
                        resp = Skipper.TrLink(url)
                    
                    elif url.split('/')[2] in config.domains['pndtl']:
                        
                        resp = Skipper.PndTl(url)
                    
                    elif url.split('/')[2] in config.domains['ouo']:
                        
                        resp = Skipper.Ouo(url)
                    
                    else:

                        utils.write_wfp(

                            f"{Fore.LIGHTMAGENTA_EX}[ {Fore.LIGHTYELLOW_EX}{channel} {Fore.LIGHTMAGENTA_EX}] {Fore.LIGHTRED_EX}{url} {Fore.LIGHTGREEN_EX}-> {Fore.LIGHTRED_EX}Bu linki şuan geçemiyorum",
                            "custom",
                            True

                        )
                        
                    
                    
                    if resp != 'damn':
    
                        utils.write_wfp(

                            f"{Fore.LIGHTMAGENTA_EX}[ {Fore.LIGHTYELLOW_EX}{channel} {Fore.LIGHTMAGENTA_EX}] {Fore.LIGHTRED_EX}{url} {Fore.LIGHTGREEN_EX}-> {Fore.LIGHTCYAN_EX}{resp}",
                            "custom",
                            True

                        )
                        utils.SaveTxt(channel, url, resp, link)

                        utils.Sender(channel, url, resp, msg, message.message_id, message.chat.id, link)
                        
                        channel_message = f"<b>{channel}\n\n\n{msg}\n\n\n🔗 Kısa Link: {url}\n✅ Link: {resp}</b>"

                        if config.send_to['telegram']['status']:
                            
                            for chat in config.send_to['telegram']['chat']:
                                
                                await client.send_message(

                                    chat,
                                    channel_message,
                                    parse_mode = "html",
                                    disable_web_page_preview = False

                                )
                        
                        if config.send_to['telegram']['Forward']['status']:
                            
                            for chat in config.send_to['telegram']['Forward']['chat']:
                                
                                await message.forward(chat)
                        



                        
        except Exception as e:
            
            pass # kendinize göre ekleyin
            # print(message)
            # print(e)
            # print(e.__traceback__.tb_lineno )

app.run()