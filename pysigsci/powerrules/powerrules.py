"""
Signal Sciences Rule Pack Client
"""

from __future__ import print_function
import sys
import os
import json
import tempfile
import requests

class PowerRules(object):
    """
    Class for Signal Sciences Rule Packs
    """

    INDEX = 'https://raw.githubusercontent.com/foospidy/sigsci-power-rules/master/index.json'
    GIT_URL = 'https://github.com/foospidy/sigsci-power-rules.git'
    REPO_DIR = '{}/sigsci-power-rules'.format(tempfile.gettempdir())

    def get_list(self):
        """
        Get list of power rules
        """
        index = requests.get(self.INDEX)

        if index.status_code != 200:
            print('Error retreiving power rules index.')
            sys.exit(1)

        return json.loads(index.text)['rule-packs']

    def print_list(self):
        """
        Print list of power rules
        """
        count = 1
        print('')
        for rule in self.get_list():
            if rule is not None:
                print('{}. {} ({})\t{}'.format(count,
                                               rule['display_name'],
                                               rule['name'],
                                               rule['description']))
                count += 1
        print('')

    def deploy_rule_pack(self, sigsciapi, rulepack, cli=False):
        """
        Deploy a rule pack
        """
        from git import Repo
        import glob

        response = {}
        success = True
        messages = ''

        if os.path.exists(self.REPO_DIR):
            try:
                repo = Repo(self.REPO_DIR)
                origin = repo.remotes.origin
                origin.pull()
            except Exception as error:
                print('Error updating repo: {}'.format(error))
        else:
            Repo.clone_from(self.GIT_URL, self.REPO_DIR)

        custom_signals = glob.glob('{}/power-rules-{}/custom-signals*.json'.format(self.REPO_DIR,
                                                                                   rulepack))
        custom_alerts = glob.glob('{}/power-rules-{}/custom-alerts*.json'.format(self.REPO_DIR,
                                                                                 rulepack))
        rule_lists = glob.glob('{}/power-rules-{}/rule-lists*.json'.format(self.REPO_DIR,
                                                                           rulepack))
        request_rules = glob.glob('{}/power-rules-{}/request-rules*.json'.format(self.REPO_DIR,
                                                                                 rulepack))
        signal_rules = glob.glob('{}/power-rules-{}/signal-rules*.json'.format(self.REPO_DIR,
                                                                               rulepack))
        templated_rules = glob.glob('{}/power-rules-{}/templated-rules*.json'.format(self.REPO_DIR,
                                                                                     rulepack))
        advanced_rules = glob.glob('{}/power-rules-{}/advanced-rules*.json'.format(self.REPO_DIR,
                                                                                   rulepack))

        for custom_signal in custom_signals:
            try:
                with open(custom_signal) as rule_file:
                    json_data = rule_file.read()

                    message = '\t{}'.format(custom_signal.replace('{}/power-rules-{}/'.format(
                        self.REPO_DIR, rulepack), ''))

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_custom_signals(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))

                if cli:
                    print(message)

                messages += message

        for custom_alert in custom_alerts:
            try:
                with open(custom_alert) as rule_file:
                    json_data = rule_file.read()

                    message = '\t{}'.format(custom_alert.replace('{}/power-rules-{}/'.format(
                        self.REPO_DIR, rulepack), ''))

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_custom_alert(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))

                if cli:
                    print(message)

                messages += message

        for rule_list in rule_lists:
            try:
                with open(rule_list) as rule_file:
                    json_data = rule_file.read()

                    message = '\t{}'.format(rule_list.replace('{}/power-rules-{}/'.format(
                        self.REPO_DIR, rulepack), ''))

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_rule_lists(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))

                if cli:
                    print(message)

                messages += message

        for request_rule in request_rules:
            try:
                with open(request_rule) as rule_file:
                    json_data = rule_file.read()

                    message = '\t{}'.format(request_rule.replace('{}/power-rules-{}/'.format(
                        self.REPO_DIR, rulepack), ''))

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_request_rules(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))

                if cli:
                    print(message)

                messages += message

        for signal_rule in signal_rules:
            try:
                with open(signal_rule) as rule_file:
                    json_data = rule_file.read()

                    message = '\t{}'.format(signal_rule.replace('{}/power-rules-{}/'.format(
                        self.REPO_DIR, rulepack), ''))

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_signal_rules(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))

                if cli:
                    print(message)

                messages += message

        for templated_rule in templated_rules:
            try:
                with open(templated_rule) as rule_file:
                    json_data = rule_file.read()

                    message = '\t{}'.format(templated_rule.replace('{}/power-rules-{}/'.format(
                        self.REPO_DIR, rulepack), ''))

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_templated_rules(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))

                if cli:
                    print(message)

                messages += message

        for advanced_rule in advanced_rules:
            try:
                with open(advanced_rule) as rule_file:
                    json_data = rule_file.read()

                    advanced_rule_file = '{}'.format(
                        advanced_rule.replace('{}/power-rules-{}/'.format(
                            self.REPO_DIR, rulepack), ''))

                    message = '\t{}'.format(advanced_rule_file)

                    if cli:
                        print(message)

                    messages += message

                    sigsciapi.add_advanced_rules(json.loads(json_data))

            except Exception as error:
                success = False
                message = '\t\t{}'.format(str(error))
                message += '\n\t\tIf you do not have permissions to deploy advanced rules,'
                message += '\n\t\tsend email to support@signalsciences.com requesting to deploy'
                message += '\n\t\t{} to {}'.format(
                    self.GIT_URL.replace('.git',
                                         '/master/power-rules-{}/{}'
                                         .format(rulepack,
                                                 advanced_rule_file)),
                    sigsciapi.site).replace('github.com',
                                            'raw.githubusercontent.com')

                if cli:
                    print(message)

                messages += message

        response['success'] = success
        response['messages'] = messages

        return response
