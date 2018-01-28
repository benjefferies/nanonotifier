# Raiblock payments
A simple app to notify (print to console) of any payments incoming payments

## Raiblocks node
Setup raiblocks node by following https://1xrb.com/support-the-network/

## Setup
```bash
pipenv install
python run.py "[::1]" "xrb_youraddress"
```

The output looks something like

```
New transaction from xrb_youraddress for 400000000000000000000000000
New transaction from xrb_youraddress for 200000000000000000000000000
New transaction from xrb_youraddress for 300000000000000000000000000
New transaction from xrb_youraddress for 1000000000000000000000000000
New transaction from xrb_youraddress for 100000000000000000000000000
```