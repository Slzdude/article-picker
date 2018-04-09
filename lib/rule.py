# coding:utf-8
import datetime
import re

from lib.filter import Filter


class Rule:
    def __init__(self, rule, method=1, debug=True):
        if type(rule) is not dict:
            raise Exception('Error 01')

        if 'name' not in rule.keys():
            raise Exception('Error 02')

        if 'url' not in rule.keys():
            raise Exception('Error 03')

        self.method = method

        self.replace = {
            'data-src': 'src',
            '</?p .*?>': '',
            '</?span.*?>': '',
            '</?script.*?>': '',
            '</?div.*?>': '',
            '<noscript.*?/noscript>': '',
            '\\r\\n\\r\\n': '\\r\\n',
        }

        self.header = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'tags': '[]',
            'categories': '收藏'
        }

        self.content = {}

        self._content = None
        self._header = None

        _hs = ['header', 'content', 'replace']
        for _h in _hs:
            if _h in rule.keys():
                _t = rule[_h]
                if type(_t) is dict:
                    getattr(self, _h).update(_t)
                else:
                    raise Exception('Error 04')
        self.rule = rule
        self.debug = debug

    def match(self, url):
        if 'url' not in self.rule.keys():
            raise Exception('Error 03')

        if 'regex' in self.rule.keys():
            if self.rule['regex'] is True:
                return re.search(self.rule['url'], url, re.I) is not None
        return url.find(self.rule['url']) > -1

    def _merge_header(self, hs):
        header = '---\r\n'
        for k in hs:
            header += '%s: %s\r\n' % (k, hs[k])
        header += '---\r\n\r\n'
        return header

    def _clean(self, data):
        for ori, aft in self.replace.items():
            data = re.sub(ori, aft, data, re.I | re.S | re.M)
        return data

    def get_header(self, data):
        ret = {}
        for k, v in self.header.items():
            if type(v) is str:
                if '(' in v and ')' in v:
                    _r = re.findall(v, data)
                    if len(_r) > 0:
                        ret[k] = _r[0]
                        continue
                ret[k] = v
            elif type(v) is dict:
                if 'value' in v.keys():
                    _r = re.findall(v['value'], data)
                    if len(_r) == 0:
                        continue
                    _tmp = _r[0]
                    if 'filter' in v.keys():
                        if type(v['filter']) is list:
                            for _f in v['filter']:
                                if hasattr(Filter, _f):
                                    _tmp = getattr(Filter, _f)(_tmp)
                                else:
                                    raise ('Filter %s not found' % _f)
                    ret[k] = _tmp
            else:
                raise Exception('Unknown type: ' + type(v))
        self._header = self._merge_header(ret)
        if self.debug:
            print(self._header)
        return self._header

    def get_content(self, data):
        if 'begin' in self.content.keys() or 'end' in self.content.keys():
            _begin = data.find(self.content['begin'])
            if _begin != -1:
                data = data[_begin + len(self.content['begin']):]
            _end = data.find(self.content['end'])
            if _end != -1:
                data = data[:_end]
        result = data
        result = self._clean(result)
        if self.method == 1:
            from lib.basic_html2text import html2text
            result = html2text(result)
        elif self.method == 2:
            from lib.html2text import html2text
            result = html2text(result)
        else:
            from lib.antimarkdown import to_markdown
            result = to_markdown(result)
        self._content = result
        return result

    def write_out(self, path, content):
        with open(path, 'wb') as fp:
            if self._header is not None:
                fp.write(self._header.encode('UTF-8'))
            if self._content is None:
                self.get_content(content)
            fp.write(self._content.encode('UTF-8'))
