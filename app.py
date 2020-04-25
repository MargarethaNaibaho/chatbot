import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('JlI0+H9LXkMYXtrsyYPPlfxz2cQ3erli/MvVKT2+L1Ebne/7RjeKAx/lzG95VNOzW1gZ2WAZoyP6v8B1mVvnx9UJ99TFc4KMzmP2MBgLvCsYGyyLPR2c5fmvwT4hAdl0XBVEbbga7pA9DAYIyavQrAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c4caeb1369aee770664207f52ee6cf20')

URL = "https://covid19.pemkomedan.go.id/index.php?page=stat_kec"
r = requests.get(URL) 
soup = BeautifulSoup(r.content, 'html5lib')
TJ=[] 
table = soup.find('tbody') 
    
for row in table.findAll('tr'):
    
    # Deklarasi variabel
    tj = {}
   
    # Memasukkan value ke tanya-jawab
    tj['no'] = row.findAll('td')[0].text
    tj['kecamatan'] = row.findAll('td')[1].text
    tj['ODP'] = row.findAll('td')[2].text
    tj['OTG'] = row.findAll('td')[3].text
    tj['PP'] = row.findAll('td')[4].text
    tj['PDP'] = row.findAll('td')[5].text
    tj['Positif'] = row.findAll('td')[6].text
    tj['Meninggal'] = row.findAll('td')[7].text
    tj['Sembuh'] = row.findAll('td')[8].text
    
    # Menambahkan baris baru anime ke list animes
    TJ.append(tj)

# Memasukkan data Tanya-Jawab ke dataframe
df = pd.DataFrame(TJ)
df = df[['no','kecamatan','ODP','OTG','PP','PDP','Positif','Meninggal','Sembuh']]
df.to_csv('data.csv', mode='w', index=False)

data = pd.read_csv('data.csv')
    
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
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """" Here's all the messages will be handled and processed by the program """
    
    msg = (event.message.text).lower()
    kembali = "Menu. Kembali ke Menu utama"

    if 'menu' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Pilih Provinsi: \n\nA. Medan Amplas\n\nB. Medan Area\n\nC. Medan Barat\n\nD. Medan Baru\n\nE. Medan Belawan\n\nF. Medan Deli\n\nG. Medan Denai\n\nH. Medan Helvetia\n\nI. Medan Johor\n\nJ. Medan Kota\n\nK. Medan Labuhan\n\nL. Medan Maimun\n\nM. Medan Marelan\n\nN. Medan Perjuangan\n\nO. Medan Petisah\n\nP. Medan Polonia\n\nQ. Medan Selayang\n\nR. Medan Sunggal\n\nS. Medan Tembung\n\nT. Medan Timur\n\nU. Medan Tuntungan\n\n\nMenu. Menu"),
        TextSendMessage(text="Ketik pilihan yang ingin Anda pilih. Misal: Ketik A untuk mengetahui Data Covid-19 Kecamatan Medan Amplas")
        ])
    elif 'a' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[0],['kecamatan']]+"\nPositif: "+data.loc[[0],['Positif']]+"\nSembuh: "+data.loc[[0],['Sembuh']]+"\nMeninggal: "+data.loc[[0],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'b' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[1],['kecamatan']]+"\nPositif: "+data.loc[[1],['Positif']]+"\nSembuh: "+data.loc[[1],['Sembuh']]+"\nMeninggal: "+data.loc[[1],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'c' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[2],['kecamatan']]+"\nPositif: "+data.loc[[2],['Positif']]+"\nSembuh: "+data.loc[[2],['Sembuh']]+"\nMeninggal: "+data.loc[[2],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'd' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[3],['kecamatan']]+"\nPositif: "+data.loc[[3],['Positif']]+"\nSembuh: "+data.loc[[3],['Sembuh']]+"\nMeninggal: "+data.loc[[3],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'e' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[4],['kecamatan']]+"\nPositif: "+data.loc[[4],['Positif']]+"\nSembuh: "+data.loc[[4],['Sembuh']]+"\nMeninggal: "+data.loc[[4],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'f' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[5],['kecamatan']]+"\nPositif: "+data.loc[[5],['Positif']]+"\nSembuh: "+data.loc[[5],['Sembuh']]+"\nMeninggal: "+data.loc[[5],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'g' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[6],['kecamatan']]+"\nPositif: "+data.loc[[6],['Positif']]+"\nSembuh: "+data.loc[[6],['Sembuh']]+"\nMeninggal: "+data.loc[[6],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'h' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[7],['kecamatan']]+"\nPositif: "+data.loc[[7],['Positif']]+"\nSembuh: "+data.loc[[7],['Sembuh']]+"\nMeninggal: "+data.loc[[7],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'i' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[8],['kecamatan']]+"\nPositif: "+data.loc[[8],['Positif']]+"\nSembuh: "+data.loc[[8],['Sembuh']]+"\nMeninggal: "+data.loc[[8],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'j' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[9],['kecamatan']]+"\nPositif: "+data.loc[[9],['Positif']]+"\nSembuh: "+data.loc[[9],['Sembuh']]+"\nMeninggal: "+data.loc[[9],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'k' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[10],['kecamatan']]+"\nPositif: "+data.loc[[10],['Positif']]+"\nSembuh: "+data.loc[[10],['Sembuh']]+"\nMeninggal: "+data.loc[[10],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'l' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[11],['kecamatan']]+"\nPositif: "+data.loc[[11],['Positif']]+"\nSembuh: "+data.loc[[11],['Sembuh']]+"\nMeninggal: "+data.loc[[11],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'm' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[12],['kecamatan']]+"\nPositif: "+data.loc[[12],['Positif']]+"\nSembuh: "+data.loc[[12],['Sembuh']]+"\nMeninggal: "+data.loc[[12],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'n' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[13],['kecamatan']]+"\nPositif: "+data.loc[[13],['Positif']]+"\nSembuh: "+data.loc[[13],['Sembuh']]+"\nMeninggal: "+data.loc[[13],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'o' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[14],['kecamatan']]+"\nPositif: "+data.loc[[14],['Positif']]+"\nSembuh: "+data.loc[[14],['Sembuh']]+"\nMeninggal: "+data.loc[[14],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'p' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[15],['kecamatan']]+"\nPositif: "+data.loc[[15],['Positif']]+"\nSembuh: "+data.loc[[15],['Sembuh']]+"\nMeninggal: "+data.loc[[15],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'q' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[16],['kecamatan']]+"\nPositif: "+data.loc[[16],['Positif']]+"\nSembuh: "+data.loc[[16],['Sembuh']]+"\nMeninggal: "+data.loc[[16],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'r' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[17],['kecamatan']]+"\nPositif: "+data.loc[[17],['Positif']]+"\nSembuh: "+data.loc[[17],['Sembuh']]+"\nMeninggal: "+data.loc[[17],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 's' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[18],['kecamatan']]+"\nPositif: "+data.loc[[18],['Positif']]+"\nSembuh: "+data.loc[[18],['Sembuh']]+"\nMeninggal: "+data.loc[[18],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 't' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[19],['kecamatan']]+"\nPositif: "+data.loc[[19],['Positif']]+"\nSembuh: "+data.loc[[19],['Sembuh']]+"\nMeninggal: "+data.loc[[19],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    elif 'u' in msg:
        line_bot_api.reply_message(
        event.reply_token, [
        TextSendMessage(text="Data Covid-19 di Kecamatan"+data.loc[[20],['kecamatan']]+"\nPositif: "+data.loc[[20],['Positif']]+"\nSembuh: "+data.loc[[20],['Sembuh']]+"\nMeninggal: "+data.loc[[20],['Meninggal']]),
        TextSendMessage(text=kembali)
        ])
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="kembali"))
    

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
