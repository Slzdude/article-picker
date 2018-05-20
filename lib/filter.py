# coding: utf-8
import time
import re
import requests


def list_strip(data):
    return [re.sub('</?p.*?>','',x,flags=re.S|re.I).strip() for x in data]


class Filter:
    @staticmethod
    def ts2dt(value):
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(int(value))
        dt = time.strftime(format, value)
        return dt

    @staticmethod
    def table(value):
        tables = re.findall('<table.+?</table>', value, re.S)
        for t in tables:
            heads = list_strip(re.findall(r'<th\b.*?>(.+?)</th>', t, re.S))
            body = re.findall('<tbody.+?</tbody>', t, re.S)[0]
            datas = list_strip(re.findall('<tr.*?>(.+?)</tr>', body, re.S))
            result = '| %s |<br>' % ' | '.join(heads)
            result += '|%s<br>' % ('--|' * len(heads))
            for d in datas:
                result += '| %s |<br>' % ' | '.join(list_strip(re.findall('<td.*?>(.+?)</td>', d,re.S)))

            # print(result.replace('<br>','\n'))
            value = value.replace(t, result)
        return value


