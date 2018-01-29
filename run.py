import sys

import requests
import time
import json


host = sys.argv[1]
account = sys.argv[2]
data = {
    'action': 'account_history',
    'account': account,
    'count': 10,
}


def get_trans_history():
    return requests.post(f'http://{host}:7076', json.dumps(data)).json().get('history', [])


last_known_trans = get_trans_history()
while True:
    trans_history = get_trans_history()
    new_trans = [x for x in trans_history if x not in last_known_trans]
    total = 0
    message = ''
    for tran in new_trans:
        if tran['type'] == 'receive':
            account = tran['account']
            amount = float(tran['amount'])
            if amount != 0:
                amount /= 1.0e+30
            total += amount
            message += f'New transaction from {account} for ' + "{:10.5f}\n".format(amount)

    if total > 0:
        subject = 'Received {:10.5f} XRB'.format(total)
        print(subject)
        print(message)
    last_known_trans = trans_history
    time.sleep(5)

