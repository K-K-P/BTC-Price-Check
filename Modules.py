import requests
import json
import smtplib
from email.message import EmailMessage


def get_data(url, headers, params):
    """Obtain data from coinmarketcap API and return recent BTC price and its 90-days change of rate"""
    response = requests.get(url, params=params, headers=headers)
    data = json.loads(response.text)
    btc_data = data['data'][0]
    btc_price = btc_data['quote']['PLN']['price']
    btc_change90d = str(btc_data['quote']['PLN']['percent_change_90d'])
    return btc_price, btc_change90d

def create_message(to_name, time, quote, price_change, to_address='XXXXXXX@XXXX.com', me='XXXXX@XXXXX.com'):
    """Depending on increase of decrease of the BTC price send adequate message with use of the template below"""
    msg = EmailMessage()  # Message object
    msg['Subject'] = 'BTC price, {}'.format(to_name)
    msg['From'] = me
    msg['To'] = to_address
    if price_change[0] == '-':
        msg.set_content('''
        Hi, {0}!
        Here is the recent value of BTC cryptocurrency:
        Time           Value [PLN]
        {1}            {2}
        Bitcoin has dropped in value by: {3} % within last 90 days
        '''.format(to_name, str(time)[:19], quote, price_change))  # Set content of a message (raw string)
    if price_change[0] != '-':
        msg.set_content(r'''
        Hi, {0}! 
        Here is the recent value of BTC cryptocurrency:
        Time Value [PLN]
        {1}  {2:.2f}
        Bitcoin has increased in value by: {3:.6} % within last 90 days
        '''.format(to_name, time, quote, price_change))  # Set content of a message (raw string)
    return msg


def send_message(message, password='XXXXXXX', host='XXXXXXX', port='XXX', user='XXXXXX@XXXXXXX.com'):
    """Send message with credentials as given above - hiding credentials in conf file - to be implemented"""
    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(user, password)
        server.send_message(message)
        server.quit()

def iftt_notification(iftt_url, value1, value2, event='BTC Price'):
    """Send a notification to smartphone using IFTTT app
    Notifications are given in 'data' dictionary - up to 3 values possible
    In default value1 is a current BTC price, value2 is 90-days change rate of BTC"""
    data = {'Value1': value1, 'Value2': value2}
    iftt_url = iftt_url.format(event)
    request = requests.post(iftt_url, json=data)
    print(request)