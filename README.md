# RaiBlocks payment notifier
A simple app to notify (print to console) of any incoming RaiBlocks payments

## RaiBlocks node
Setup raiblocks node by following https://1xrb.com/support-the-network/

## Setup for Mac
```bash
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
sudo easy_install pip
pip install pipenv
wget https://github.com/benjefferies/raiblockpayments/archive/master.zip
unzip master.zip
cd raiblockpayments-master/
pipenv install
pipenv run python run.py
```

## Setup (Ubuntu Example - append sudo if not root)
```bash
apt update
apt install python-pip unzip
curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
pip install pipenv
wget https://github.com/benjefferies/raiblockpayments/archive/master.zip
unzip master.zip
cd raiblockpayments-master/
pipenv install
pipenv run python run.py
```

## Sending email notifications
Emails are sent via [AWS SES](https://aws.amazon.com/ses/). You get a 62,000 emails for free per month.
1. Verify the email e.g. `myemail@mydomain.com` you want to send from https://us-west-2.console.aws.amazon.com/ses/home?region=us-west-2#verified-senders-email:
2. Update the [.env](.env) variables to look like
```
EMAIL_ENABLED=True
AWS_REGION=us-west-2
SES_SOURCE_EMAIL=myemail@mydomain.com
```
3. Set the AWS credential environmental variables
```bash
export AWS_ACCESS_KEY_ID=notsosecret # YOUR ACCESS_KEY
export AWS_SECRET_ACCESS_KEY=verysecret # YOUR SECRET_ACCESS
```
4.
```bash
pipenv run python run.py
```