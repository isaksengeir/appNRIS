import csv
from datetime import datetime, timedelta


# Static methods
colors = {"blue": "#2e54ff", "green": "#08a91e", "orange": "#ff5733"}


def read_roster_csv(filepath):
    title = None
    header = None
    table = list()
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if header:
                table.append(row)
            if not title and len(row) == 1:
                title = str(row[0])
            if not header and len(row) > 1:
                header = row

    return title, header, table


def week_to_date(year, week):
    """
    converts week number for a given year to date (year-month-day)
    :param year: int
    :param week: int
    :return: first date, last date of week (year-month-day)
    """
    firstdayofweek = datetime.strptime(f'{year}-W{int(week)}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + timedelta(days=6.9)
    return firstdayofweek, lastdayofweek


def event_body():
    body = {
        'summary': f'New event',
        'location': "https://rt.uninett.no & https://slack.com/intl/en-no/",
        'description': 'https://gitlab.sigma2.no/sigma2/interndokumentasjon/-/tree/master/support',
        'start': {
            'date': "",
            'timeZone': 'GMT+02:00',
        },
        'end': {
            'date': "",
            'timeZone': 'GMT+02:00',
        },
        'attendees': [],
        'reminders': {
            'useDefault': 'useDefault',
        },
        "colorId": 8,
        "anyoneCanAddSelf": True,
        "sendUpdates": "all",
        "sendNotifications": True,
    }
    return body