# RaiBlocks payment notifier
A simple app to notify (print to console) of any incoming RaiBlocks payments

## RaiBlocks node
Setup raiblocks node by following https://1xrb.com/support-the-network/

## Setup (Ubuntu Example - append sudo if not root)
```bash
apt update
apt install python-pip unzip
pip install pipenv
wget https://github.com/raitheon/raiblockpayments/archive/master.zip
unzip master.zip
cd raiblockpayments-master/
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
