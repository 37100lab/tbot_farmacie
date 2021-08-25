from telegram import *
from telegram.ext import *
import math as m
import psycopg2, json, time

def dist(lat1,lon1, lat2, lon2):
    return 6371 * 2 * m.asin(m.sqrt(m.pow(m.sin((m.radians(lat2) - m.radians(lat1)) / 2), 2) + m.cos(lat1) * m.cos(lat2) * m.pow(m.sin((m.radians(lon2) - m.radians(lon1)) / 2), 2)))

def start(update: Update, context: CallbackContext) -> None:
    testo = "Benvenuto!!!\nQuesto bot ti permette di trovare la farmacia più vicina a te.\nInvia la tua posizione."
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo)

def distanza(update: Update, context: CallbackContext) -> None:
    try:
        lat1 = update.message.location.latitude
        lon1 = update.message.location.longitude
        d = []
        for i in range(0,len(coord_x)):
            d.append(dist(lat1,lon1,coord_x[i],coord_y[i]))
        e = d[:]
        d.sort()
        ind = 0
        for i in range(0,len(d)):
            if d[0]==e[i]:
                ind = i
                break
        testo = "La farmacia più vicina è: " + nome[ind]
        testo_dist = "\nDistanza: " + str(round(d[0],2)) + " km"
        testo_ind = "\nIndirizzo: " + indirizzi[ind]
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo+testo_dist+testo_ind)
        update.message.reply_location(coord_x[ind], coord_y[ind])
        testo = "Per trovare nuovamente la farmacia più vicina invia la tua posizione."
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo)
    except:
        testo_try = "Attenzione!!!\nInviare solo la posizione attuale.\nInterrompere la condivisione della posizione in tempo reale."
        context.bot.send_message(chat_id=update.effective_chat.id, text=testo_try)

def echo(update: Update, context: CallbackContext) -> None:
    testo = "Non è un comando valido."
    context.bot.send_message(chat_id=update.effective_chat.id, text=testo)

def main():
    updater = Updater("bot-id")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.location, distanza))
    updater.start_polling()
    updater.idle()

con = psycopg2.connect(
	host="host",
	database="database",
	user="user",
	password="password"
       	 )

cur = con.cursor()
v = []
coord_x = []
coord_y = []
indirizzi = []
nome = []

cur.execute("select ST_AsGeoJSON(geom) from farmacie")
a = cur.fetchall()
cur.execute("select indirizzo from farmacie")
b = cur.fetchall()
cur.execute("select denominazi from farmacie")
c = cur.fetchall()
for i in range(0,len(a)):
    v.append(json.loads(a[i][0]))
    coord_x.append(v[i]['coordinates'][1])
    coord_y.append(v[i]['coordinates'][0])
    indirizzi.append(b[i][0])
    nome.append(c[i][0])
cur.close()
con.close()
main()
