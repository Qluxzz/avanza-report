# avanza-report
Generates and sends a report about your holdings at Avanza for the last 7 days

# Setup
In order to run the script you need to create a config.ini file in the root directory with the following settings
``` ini
[GMAIL]
USERNAME='your.email@gmail.com'
PASSWORD='your_generated_gmail_app_password'
[AVANZA]
USERNAME='your_avanza_username'
PASSWORD='your_avanza_password'
TOTPSECRET='your_totp_secret, read below to find out how to generate one'
ACCOUNT_ID='avanza_account_id'
```

## Gmail password
If you have enabled 2FA for your Gmail account, you can generate an app password [here](https://support.google.com/accounts/answer/185833?hl=en) and use it

## Avanza credentails
This script uses my Python Library for Avanza, which you can find here https://github.com/Qluxzz/avanza.

In the readme you can find out how to generate your ``` TOTPSECRET ```
