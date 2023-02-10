from dateutil.relativedelta import relativedelta
import datetime as dt
start = dt.date(2020, 2, 3)
rel = relativedelta(months=12)
dd = start - rel
print(dd.month)