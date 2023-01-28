import requests
import datetime
from twilio.rest import Client

#config twilio client
account_sid = 'twilio account sid'
auth_token = 'twilio auth token'

client = Client(account_sid, auth_token)


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

#day finder
time = datetime.datetime.now()
year = time.year
month = time.month
day = time.day
current_day = f'{year}-{month}-{day}'

#api parametrs
api_key_news = '*********************'
api_key_stock = '****************'
parameter_stock = {
    'function':'TIME_SERIES_DAILY_ADJUSTED',
    'symbol':STOCK,
    'apikey':api_key_stock
}
parameter_news = {
    'q':COMPANY_NAME,
    'from':current_day,
    'sortBy':'popularity',
    'apiKey':api_key_news
}

#get stock information
url = 'https://www.alphavantage.co/query'
r = requests.get(url, params=parameter_stock)
data = r.json()['Time Series (Daily)']

list = [v for (n,v) in data.items()]
start_day = list[0]['1. open']
end_day = list[0]['4. close']
#calculate delta value percent
percent = (float(end_day) * 100)/float(start_day)
delta_percent = percent - 100

#get news information
url_new = 'https://newsapi.org/v2/everything'
resp = requests.get(url_new, params=parameter_news)
data_news = resp.json()['articles']
three_data = data_news[:3]

#send sms
if round(delta_percent,2) > 0:
    for i in range(0,3):
        message = client.messages.create(
                    body=f"""TSLA: ⏫{round(delta_percent,2)}%\nHeadline: {three_data[i]['title']}\nBrief: {three_data[i]['description']}
                    """,
                    from_='YOUR_TWILO NUMBER',
                    to='NUMBER_WHERE_YOU_WANT_TO_RECIVE_SMS'
                )
       
else:
    for i in range(0,3):
        message = client.messages.create(
                    body=f"""TSLA: ⏬{abs(round(delta_percent,2))}%\nHeadline: {three_data[i]['title']}\nBrief: {three_data[i]['description']}
                    """,
                    from_='YOUR_TWILO NUMBER',
                    to='NUMBER_WHERE_YOU_WANT_TO_RECIVE_SMS'
                )