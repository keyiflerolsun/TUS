from Data import config

import requests

def Send(title, desc, ShortUrl, FinishUrl, link):
    
    data = {
    
        "username": "UrlSkipper",
        "avatar_url": "https://cdn.discordapp.com/attachments/951597393042878535/951597515222970388/6cd9532babc72c1dc7033fa824d15cf7.png",
        "content": "",
        "embeds": [
            
            {
                "title": title,
                "color": 64511,
                "description": desc,
                "url": "https://www.youtube.com/c/WarForPeace_YT/",
                "author": {
                    
                    "name": "UrlSkipper",
                    "url": "https://www.youtube.com/c/WarForPeace_YT/",
                    "icon_url": "https://cdn.discordapp.com/attachments/951597393042878535/951597515222970388/6cd9532babc72c1dc7033fa824d15cf7.png"
               
                },
               
                "image": {},
                "thumbnail": {},
                "footer": {
               
                    "icon_url": "https://cdn.discordapp.com/attachments/951597393042878535/951597515222970388/6cd9532babc72c1dc7033fa824d15cf7.png"
               
                },
               
                "fields": [

                    {

                        "name": "Mesaja git",
                        "value": link,
                        "inline": False

                    },
                    
                    {

                        "name": "Kısa Link",
                        "value": ShortUrl,
                        "inline": False

                    },
                    
                    {

                        "name": "Link",
                        "value": FinishUrl,
                        "inline": False

                    }

                ]
            
            }
        
        ],
        
        "components": [
        
            {
                "type": 1,
                "components": [
                    
                    {
                    
                        "type": 2,
                        "style": 5,
                        "label": "Kısa Linke Git",
                        "url": ShortUrl
                    
                    },
                    
                    {
                    
                        "type": 2,
                        "style": 5,
                        "label": "Linke Git",
                        "url": FinishUrl
                    
                    }
    
                ]
    
            }
   
        ]
   
    }
    
    for webhook in config.send_to['discord']['webhook']:
        
        r = requests.post(

            webhook,
            json = data

        )