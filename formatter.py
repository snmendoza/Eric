from money import Money


def as_date(date):
    return date.strftime('%d %B, %Y')


def as_time(time):
    return time.strftime('%M:%H')


def as_money(value):
    m = Money(value, 'ARS')
    return m.format('es_AR')
