# coding:utf-8

import json
import os

from lib.rule import Rule


class RulesManager(object):
    """Plugin manager that loads plugins from plugin directories.
    """

    def __init__(self):
        self.rules = []
        self.path = os.getcwd()

        with open(os.path.join(self.path, "rule.json"), encoding='UTF-8') as fp:
            i = 0
            rule_list = json.loads(fp.read())

            for _rule in rule_list['rules']:
                try:
                    rule = Rule(_rule)
                    self.rules.append(rule)
                    i = i + 1
                except Exception as e:
                    print(_rule['name'] + ' error: ' + str(e))
        print("%d rules load success." % i)

    def match(self, url):
        for rule in self.rules:
            if rule.match(url):
                print('Rule Matches: ' + rule.rule['name'])
                return rule
        return None
