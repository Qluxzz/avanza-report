import configparser
import os
import json
import smtplib
from datetime import date

from jinja2 import Environment, FileSystemLoader, select_autoescape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from avanza import Avanza, CONSTANTS

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

CONFIG = configparser.ConfigParser()
CONFIG.read(ROOT_PATH + '/config.ini')

TEMPLATE_ENVIRONMENT = Environment(
    loader=FileSystemLoader(os.path.join(ROOT_PATH, 'templates')),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=True,
    lstrip_blocks=True
)

def send_mail(subject, data):
    from_address = 'rapport@avanza.se'
    to_address = CONFIG['GMAIL']['USERNAME']

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    html = MIMEText(data, 'html', "utf-8")
    msg.attach(html)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(CONFIG['GMAIL']['USERNAME'], CONFIG['GMAIL']['PASSWORD'])
    server.sendmail(from_address, to_address, msg.as_string())
    server.close()

def get_positions_by_outcome(data):
    instruments = data['developmentResponse']['instruments']

    positions = []
    for instrument in instruments:
        for position in instrument['positions']:
            positions.append({
                'name': position['shortName'],
                'outcomeTotal': position['outcome']['total'],
                'outcomePercent': position['outcome']['totalDevelopmentInPercent']
            })

    positions.sort(
        key=lambda position: position['outcomePercent'],
        reverse=True
    )

    return positions

def get_avanza_weekly_report():
    avanza = Avanza({
        'username': CONFIG['AVANZA']['USERNAME'],
        'password': CONFIG['AVANZA']['PASSWORD'],
        'totpSecret': CONFIG['AVANZA']['TOTPSECRET']
    })

    account_id = CONFIG['AVANZA']['ACCOUNT_ID']

    data = avanza.get_insights_report(
        CONSTANTS['public']['ONE_WEEK'],
        account_id
    )

    total_development = data['developmentResponse']['totalOutcome']['total']

    date_range = '{} - {}'.format(
        data['fromDate'],
        date.today().strftime('%Y-%m-%d')
    )

    positions = get_positions_by_outcome(data)

    return {
        'total_development': total_development,
        'positions': positions,
        'date_range': date_range
    }

def render_html_template(data):
    template = TEMPLATE_ENVIRONMENT.get_template('index.html')
    return template.render(data)


def main():
    weekly_rapport_data = get_avanza_weekly_report()

    subject = 'Veckorapport från Avanza, {}'.format(
        weekly_rapport_data['date_range']
    )

    html = render_html_template(weekly_rapport_data)

    send_mail(subject, html)

if __name__ == "__main__":
    main()
