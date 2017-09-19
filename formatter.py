from babel.dates import format_date, format_time
from money import Money


def as_date(date):
    return format_date(date, format='long', locale='es_AR')


def as_time(time):
    return time.strftime('%M:%H')


def as_money(value):
    m = Money(value, 'ARS')
    return m.format('es_AR')
