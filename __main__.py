#! python3

"""This script connects to API and retrieves the current crypto value"""
if __name__ == '__main__':

    from Modules import get_data
    from Modules import create_message
    from Modules import send_message
    from datetime import datetime
    from Modules import iftt_notification

    # URL, headers and params for coinmarketcap API:
    url_btc = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'X-CMC_PRO_API_KEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        'Accepts': 'application/json'
              }
    params = {
      'start': '1',
      'convert': 'PLN',
             }
    #URL for IFTTT trigger:
    url_ifttt = 'https://maker.ifttt.com/trigger/{0}/json/with/key/XXXXXXXXXXXXXXXXXXXXXX'

    data = get_data(url_btc, headers, params)
    btc_price = data[0]
    btc_change90d = data[1]
    time = datetime.now()
    msg = create_message('Kamil', time=time, quote=btc_price, price_change=btc_change90d)
    send_message(msg)
    iftt_notification(url_ifttt, value1=btc_price, value2=btc_change90d)



