import re

pattern_date = re.compile(r'(?P<date1>2019-\d+-\d+) (?P<date2>\d{2}:\d{2}:\d{2})')
print(re.findall(pattern_date,'2019-3-11 21:47:13'))
