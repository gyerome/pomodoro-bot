import os

TOKEN = os.environ.get('TOKEN')
IP = os.environ.get('IP')

webhook = False
webhook_params=dict(
    cert='path to cert',
    key='path to key',
    listen = IP,
    port = 80,
    url_path = TOKEN,
    webhook_url = f'https://{IP}/{TOKEN}'    
    )