import sys

import requests
import time
import json

host = sys.argv[1]
account = sys.argv[2]
trans = []
while True:
    data = {
        'action': 'account_history',
        'account': account,
        'count': 10,
    }
    resp = requests.post(f'http://{host}:7076', json.dumps(data)).json()
    new_trans = [x for x in resp['history'] if x not in trans]
    for tran in new_trans:
        if tran['type'] == 'receive':
            print('New transaction from {} for {}'.format(tran['account'], tran['amount']))
    trans = resp.get('history', [])
    time.sleep(5)

