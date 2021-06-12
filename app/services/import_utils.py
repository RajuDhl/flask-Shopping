import datetime

import pytz


def float_me_replace(val):
    try:
        return float(val.replace(',', '').replace('(', '-').replace(')', "").replace('$', '').strip())
    except (ValueError, TypeError):
        if type(val) == str and val.find('(') != -1 and val.find(')') != -1:
            num = float(val.replace(',', '').replace('(', '-').replace(')', "").replace('$', '').strip())
            return num
    except AttributeError:
        try:
            return float(val)
        except Exception as e:
            print('Error {e}')
    if val not in ('', '  ', '-', ' -   ', ' - ', '   ', '  -   '):
        print(f'Returning None for |{val}| {type(val)}')
    return 0


def percentage(val):
    if type(val) == str and val.find('%') != -1:
        return float(val.replace('%', '').strip()) * 0.01
    return None


def int_me_replace(val):
    try:
        return int(str(val).replace(',', ''))
    except ValueError:
        try:
            return int(float_me_replace(val))
        except (ValueError, TypeError):
            return 0


def build_date(d):
    if type(d) == datetime.datetime:
        print(f"returning date {d}")
        return d
    elif type(d) == str:
        try:
            x = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ")
            new_date = x.replace(hour=0, minute=1, tzinfo=pytz.timezone('US/Central'))
            print(f'new date: ' + str(new_date))
            return new_date
        except ValueError:
            try:
                x = datetime.datetime.strptime(' '.join(d.split(' ')[0:4]), "%a %b %d %Y")
                new_date = x.replace(hour=0, minute=1, tzinfo=pytz.timezone('US/Central'))
                print(f'new date: ' + str(new_date))
                return new_date
            except ValueError:
                return None


def build_date_cst(date_string):
    # import pdb;pdb.set_trace()
    cst_time_delta = datetime.timedelta(hours=-6)
    tz_object = datetime.timezone(cst_time_delta, name="CST")

    try:
        x = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        fd = datetime.datetime(x.year, x.month, x.day, 12, 59, 59, 99, tz_object)
    except ValueError:
        try:
            x = datetime.datetime.strptime(date_string, '%Y-%m/%d')
            fd = datetime.datetime(x.year, x.month, x.day, 12, 59, 59, 99, tz_object)
        except ValueError:
            try:
                x = datetime.datetime.strptime(date_string, '%m/%d/%Y')
                fd = datetime.datetime(x.year, x.month, x.day, 12, 59, 59, 99, tz_object)
            except ValueError:
                return None
    except TypeError:
        return None
    return fd


