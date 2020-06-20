def allKodeKecamatan():
    kode = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"]
    return kode

def kecamatan():
    kecamatan = ["Medan Amplas","Medan Area","Medan Barat","Medan Baru","Medan Belawan","Medan Deli","Medan Denai","Medan Helvetia","Medan Johor","Medan Kota","Medan Labuhan","Medan Maimun","Medan Marelan","Medan Perjuangan","Medan Petisah","Medan Polonia","Medan Selayang","Medan Sunggal","Medan Tembung","Medan Timur","Medan Tuntungan"]
    return kecamatan

def Menu():
    teks = "Kecamatan apa yang ingin kamu ketahui mengenai CoVid-19?\n\n"
    
    kecamatan1 = kecamatan()
    allKodeKecamatan1 = allKodeKecamatan()

    for i in range(len(kecamatan1)):
        teks += allKodeKecamatan1[i].upper() + ". " + kecamatan1[i] + "\n" 
    
    return teks

def kataSalah():
    teks = "Keyword tidak tersedia"

    return teks

def kembali():
    teks = "Ketik 'MENU' untuk ke menu utama"

    return teks

def hasilKecamatan(kodekecamatan):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np

    URL = "https://covid19.pemkomedan.go.id/index.php?page=stat_kec"
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.find('tbody') 

    No = []
    nama_kecamatan = []
    odp_kecamatan = []
    otg_kecamatan = []
    pp_kecamatan = []
    pdp_kecamatan = []
    positif_kecamatan = []
    meninggal_positif_kecamatan = []
    sembuh_kecamatan = []
    
    for i in range(len(table.findAll('tr'))):

        No.append(i+1)
        nama_kecamatan.append(table.findAll('tr')[i].findAll('td')[1].text)
        odp_kecamatan.append(table.findAll('tr')[i].findAll('td')[2].text)
        otg_kecamatan.append(table.findAll('tr')[i].findAll('td')[4].text)
        pp_kecamatan.append(table.findAll('tr')[i].findAll('td')[6].text)
        pdp_kecamatan.append(table.findAll('tr')[i].findAll('td')[10].text)
        positif_kecamatan.append(table.findAll('tr')[i].findAll('td')[13].text)
        sembuh_kecamatan.append(table.findAll('tr')[i].findAll('td')[11].text)
        meninggal_positif_kecamatan.append(table.findAll('tr')[i].findAll('td')[12].text)
   
    df_kecamatan = pd.DataFrame(No, columns =['No'])
    df_kecamatan = df_kecamatan.rename(columns={"0":"No"})
    df_kecamatan['Kecamatan'] = nama_kecamatan
    df_kecamatan['ODP'] = odp_kecamatan
    df_kecamatan['OTG'] = otg_kecamatan
    df_kecamatan['PP'] = pp_kecamatan
    df_kecamatan['PDP'] = pdp_kecamatan
    df_kecamatan['Positif'] = positif_kecamatan
    df_kecamatan['Sembuh'] = sembuh_kecamatan
    df_kecamatan['Meninggal positif'] = meninggal_positif_kecamatan

    df_kecamatan['Kode'] = allKodeKecamatan()
    is_kecamatan = df_kecamatan['Kode'].lower()==kodekecamatan
    df_cari = df_kecamatan[is_kecamatan]

    kecamatan = str(df_cari['Kecamatan'].to_string().split('    ')[1])
    odp = int(df_cari['ODP'])
    otg = int(df_cari['OTG'])
    pp = int(df_cari['PP'])
    pdp = int(df_cari['PDP'])
    positif = int(df_cari['Positif'])
    sembuh = int(df_cari['Sembuh'])
    meninggal_positif = int(df_cari['Meninggal positif'])

    teks = "Data Covid-19 di Kecamatan " + kecamatan
    teks += "ODP: " + str(odp) + "\n"
    teks += "OTG: " + str(otg) + "\n"
    teks += "PP : " + str(pp) + "\n"
    teks += "PDP: " + str(pdp) + "\n"
    teks += "Positif: " + str(positif) + "\n"
    teks += "Sembuh: " + str(sembuh) + "\n"
    teks += "Meninggal dunia (Positif): " + str(meninggal_positif) + "\n"

    return teks

import requests
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, SourceUser
)

app = Flask(__name__)

line_bot_api = LineBotApi('JlI0+H9LXkMYXtrsyYPPlfxz2cQ3erli/MvVKT2+L1Ebne/7RjeKAx/lzG95VNOzW1gZ2WAZoyP6v8B1mVvnx9UJ99TFc4KMzmP2MBgLvCsYGyyLPR2c5fmvwT4hAdl0XBVEbbga7pA9DAYIyavQrAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c4caeb1369aee770664207f52ee6cf20')
    
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """" Here's all the messages will be handled and processed by the program """
    
    msg = event.message.text.lower().replace(" ","")

    if (msg=='hai' or msg=='hi' or msg=='halo' or msg=='hello' or msg=='hey' or msg=='p'):
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Halo ' + profile.display_name)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
    
    elif msg == "menu":
        reply = Menu()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply)
            ]
        )
        
    elif msg == 'a':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'b':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'c':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'd':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
        
    elif msg == 'e':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'f':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'g':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'h':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'i':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'j':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'k':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'l':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'm':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'n':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'o':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
        
    elif msg == 'p':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
        
    elif msg == 'q':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
        
    elif msg == 'r':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 's':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 't':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    elif msg == 'u':
        reply = hasilKecamatan(msg)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
         )
    
    else:
        reply = kataSalah()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
        )

if __name__ == "__main__":
    app.run()
