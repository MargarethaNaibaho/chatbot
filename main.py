def dataIndonesia():
    from bs4 import BeautifulSoup
    import requests
    source = requests.get('https://www.kompas.com/covid-19')
    soup = BeautifulSoup(source.text, 'lxml')
    print("Terjadi kesalahan")
    data = soup.find_all('div', {'class':'covid__box2'})
    
    positif = data[0].text.split('i')[2].split(' ')[0]
    tambahan = data[0].i.text
    dirawat = data[1].text.split('t')[1].split(' ')[0]
    meninggal = data[2].text.split('l')[1].split(' ')[0]
    sembuh = data[3].text.split('h')[1].split(' ')[0]
    
    tgl_Update = soup.find('div', {'class':'covid__header'}).span.text.split(':')[1].split(',')[0]
    
    teks = "Data Covid-19 di Indonesia per" + tgl_Update + "\n"
    teks += "Positif : " + positif + "(" + tambahan + ")" + "\n"
    teks += "Dirawat : " + dirawat + "\n"
    teks += "Sembuh : " + sembuh + "\n"
    teks += "Meninggal dunia (Positif) : " + meninggal + "\n"
    
    return teks

def allKodeKecamatan():
    x = 22

    kode = []
    for i in range(1, x, 1):
        angka = str(i)
        kode.append("D"+angka)

    return kode

def kecamatan():
    kecamatan = ["Medan Amplas","Medan Area","Medan Barat","Medan Baru","Medan Belawan","Medan Deli","Medan Denai","Medan Helvetia","Medan Johor","Medan Kota","Medan Labuhan","Medan Maimun","Medan Marelan","Medan Perjuangan","Medan Petisah","Medan Polonia","Medan Selayang","Medan Sunggal","Medan Tembung","Medan Timur","Medan Tuntungan"]
    return kecamatan

def tampilNamaKecamatan():
    kode_kecamatan = allKodeKecamatan()
    nama_kecamatan = kecamatan()

    teks = "Berikut kode dan nama kecamatan\n"
    for i in range(len(kode_kecamatan)):
        teks += "[" + kode_kecamatan[i] + "]" + " " + nama_kecamatan[i] + "\n"

    teks+= "\nSilahkan masukkan kode sesuai kecamatan yang tersedia"

    return teks

def cekKecamatan(kodekecamatan):
    allKodeKecamatan1 = allKodeKecamatan()
    
    allKodeKecamatan1 = [allKodeKecamatan2.lower() for allKodeKecamatan2 in allKodeKecamatan1]
    
    return kodekecamatan in allKodeKecamatan1

def hasilKecamatan(kodekecamatan):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import time

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
    is_kecamatan = df_kecamatan['Kode']==kodekecamatan.upper()
    df_cari = df_kecamatan[is_kecamatan]

    kecamatan = str(df_cari['Kecamatan'].to_string().split('    ')[1])
    odp = int(df_cari['ODP'])
    otg = int(df_cari['OTG'])
    pp = int(df_cari['PP'])
    pdp = int(df_cari['PDP'])
    positif = int(df_cari['Positif'])
    sembuh = int(df_cari['Sembuh'])
    meninggal_positif = int(df_cari['Meninggal positif'])
    
    bulan = ("Januari", "Pebruari", "Maret","April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "Nopember", "Desember")
    hari = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")
    sekarang = time.time()
    infowaktu = time.localtime(sekarang)
    
    teks = "Data Covid-19 di Kecamatan " + kecamatan + " per " + hari[infowaktu[6]] + ", " + str(infowaktu[2]) + " " + bulan[infowaktu[1]-1] + " " + str(infowaktu[0]) + "\n"
    teks += "ODP: " + str(odp) + "\n"
    teks += "OTG: " + str(otg) + "\n"
    teks += "PP : " + str(pp) + "\n"
    teks += "PDP: " + str(pdp) + "\n"
    teks += "Positif: " + str(positif) + "\n"
    teks += "Sembuh: " + str(sembuh) + "\n"
    teks += "Meninggal dunia (Positif): " + str(meninggal_positif) + "\n"

    return teks

def allKodeProvinsi():
    x = 35
    kode = []
    for i in range(1, x, 1):
        angka = str(i)
        kode.append("C"+angka)

    return kode

def nameprovinsi():
    from bs4 import BeautifulSoup
    import requests

    source = requests.get('https://www.kompas.com/covid-19')
    soup = BeautifulSoup(source.text, 'lxml')

    nama_prov = soup.find_all('div', {'class':'covid__row'})
    nama_provinsi = []

    for i in range(len(nama_prov)):
        nama_provinsi.append(nama_prov[i].find_all('div')[0].text)

    return nama_provinsi

def cekProvinsi(kodeprovinsi):
    allKodeProvinsi1 = allKodeProvinsi()
    
    allKodeProvinsi1 = [allKodeProvinsi2.lower() for allKodeProvinsi2 in allKodeProvinsi1]
    
    return kodeprovinsi in allKodeProvinsi1

def tampilNamaProvinsi():
    kode_provinsi = allKodeProvinsi()
    nama_provinsi = nameprovinsi()

    teks = "Berikut kode dan nama provinsi\n"
    for i in range(len(kode_provinsi)):
        teks += "[" + kode_provinsi[i] + "]" + " " + nama_provinsi[i] + "\n"

    teks+= "\nSilahkan masukkan kode sesuai provinsi yang tersedia"

    return teks

def hasilProvinsi(kodeprovinsi):
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    source = requests.get('https://www.kompas.com/covid-19')
    soup = BeautifulSoup(source.text, 'lxml')
    
    nama_prov = soup.find_all('div', {'class':'covid__row'})
    tgl_Update = soup.find('div', {'class':'covid__header'}).span.text.split(':')[1].split(',')[0]

    No = []
    positif_provinsi = []
    meninggal_positif_provinsi = []
    sembuh_provinsi = []
    
    for i in range(len(nama_prov)):

        No.append(i+1)
        positif_provinsi.append(nama_prov[i].find('div', {'class':'covid__total'}).find('span', {'class':'-odp'}).text.split(' ')[1])
        meninggal_positif_provinsi.append(nama_prov[i].find('div', {'class':'covid__total'}).find('span', {'class':'-gone'}).text.split(' ')[1])
        sembuh_provinsi.append(nama_prov[i].find('div', {'class':'covid__total'}).find('span', {'class':'-health'}).text.split('  ')[1])
   
    df_provinsi = pd.DataFrame(No, columns =['No'])
    df_provinsi = df_provinsi.rename(columns={"0":"No"})
    df_provinsi['Positif'] = positif_provinsi
    df_provinsi['Sembuh'] = sembuh_provinsi
    df_provinsi['Meninggal positif'] = meninggal_positif_provinsi

    df_provinsi['Nama Provinsi'] = nameprovinsi()
    df_provinsi['Kode'] = allKodeProvinsi()

    is_provinsi = df_provinsi['Kode']==kodeprovinsi.upper()
    df_cari = df_provinsi[is_provinsi]

    provinsi = str(df_cari['Nama Provinsi'].to_string().split('    ')[1])
    positif = int(df_cari['Positif'])
    sembuh = int(df_cari['Sembuh'])
    meninggal_positif = int(df_cari['Meninggal positif'])

    teks = "Data Covid-19 di Provinsi " + str(provinsi) + " per" + tgl_Update + "\n"
    teks += "Positif: " + str(positif) + "\n"
    teks += "Sembuh: " + str(sembuh) + "\n"
    teks += "Meninggal dunia (Positif): " + str(meninggal_positif) + "\n"

    return teks

def Menu():
    teks = "Apa yang ingin kamu ketahui?\n\n"
    teks += "A. Data Covid-19 di Indonesia\n"
    teks += "C. Data Covid-19 di tiap Provinsi di Indonesia\n"
    teks += "D. Data Covid-19 di tiap Kecamatan di Kota Medan\n\n"

    teks += "Ketik kode sesuai kode yang tersedia. Contoh : Ketik 'A' untuk melihat data Covid-19 di Indonesia"
    
    return teks

def kataSalah():
    teks = "Keyword tidak tersedia"

    return teks

def kembali():
    teks = "Ketik 'MENU' untuk ke menu utama"

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
    
    elif msg == "a":
        reply = dataIndonesia()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
        )

    elif msg == "c":
        reply = tampilNamaProvinsi()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
        )

    elif msg == "d":
        reply = tampilNamaKecamatan()
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=reply),
                TextSendMessage(text=kembali())
            ]
        )

    else:
        if (cekKecamatan(msg)):
            reply = hasilKecamatan(msg)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=reply),
                    TextSendMessage(text=kembali())
                ]
            )

        elif (cekProvinsi(msg)):
            reply = hasilProvinsi(msg)
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
