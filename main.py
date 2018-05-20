# coding:utf-8
from optparse import OptionParser

import requests

from lib.rules import RulesManager

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}

proxy = {
    'http':'SOCKS5://127.0.0.1:1080',
    'https':'SOCKS5://127.0.0.1:1080'
}

if __name__ == '__main__':
    usage = "usage: %prog [-o filename] [-n] url"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--outfile", dest="outfile", metavar='FILE', help="file to write data")
    parser.add_option("-n", "--nohead", dest="nohead", action='store_true', default=False, help="do not read header")
    parser.add_option("-p", "--proxy", dest="proxy", action='store_true', default=False, help="use proxy to get content")
    parser.add_option("-l", "--local", dest="local", action='store_true', default=False, help="use local file")
    parser.add_option("-m","--method",dest="method",action="store",type="int",default=1,help="""1: Basic Html2Text Parser (DEFAULT)\n2: Forked Html2Text Parser\n3: AntiMarkdown Parser\n""")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    url = args[0]

    rules = RulesManager()
    rule = rules.match(url)
    if rule is None:
        print('No match rule found.')
        exit(0)

    if options.local:
        content = open(url).read()
    else:
        if options.proxy:
            print('Using proxy.')
            content = requests.get(url, headers=headers, proxies=proxy).text
        else:
            content = requests.get(url, headers=headers).text
    if not options.nohead:
        rule.get_header(content)
    if options.outfile:
        print('Writing result to ' + options.outfile)
        rule.write_out(options.outfile,content)
    else:
        print(rule.get_content(content))
