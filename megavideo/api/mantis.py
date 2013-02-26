#!/usr/bin/python
# -*- encoding: utf-8 -*-
from MySQLdb import escape_string, escape_dict , Connection
from datetime import datetime
from django.conf import settings

class Mantis(object):

    def __init__(self):
        dbname = getattr('MANTIS_DBNAME', settings, 'mantis')
        passwd = getattr('MANTIS_PASSWD', settings, '')
        user = getattr('MANTIS_USER', settings, '')
        host = getattr('MANTIS_HOST', settings, '')

        self.db = Connection(db = dbname, passwd = passwd, user = user, host = host)
        self.last_text_insert_id = 0
        self.last_bug_insert_id = 0

    def escape_string(self, string):
        return escape_string(string)

    def escape_dict(self, dict):
        return escape_dict(dict)

    def bug(self, **kwarg):
        """
            Default values
            #SELECT * FROM mantis_bug_table m where bug_text_id = 747
        """
        default_keys = ['project_id', 'reporter_id', 'handler_id', 'priority', \
                        'severity', 'reproducibility', 'status', 'resolution', 'projection', \
                        'category', 'date_submitted', 'last_updated', 'eta', 'bug_text_id', \
                        'os', 'os_build', 'platform', 'version', 'fixed_in_version', \
                        'build', 'profile_id', 'view_state', 'summary', 'sponsorship_total', \
                        'sticky', 'target_version']

        default_values = [24, 3, 3, 30, 50, 70, 50, 10, 10, '' , datetime.now().__str__(), datetime.now().__str__(), 10, self.last_text_insert_id, '', \
                          '', '', '', '', '', 0, 10, "Bug reportado no manager" , 0, 0, 0 ]

        default_list = zip(default_keys, default_values)

        for k, i in default_list:
            if not i in kwarg:
                kwarg[k] = i

        self.bug = kwarg

        insert = ('INSERT into mantis_bug_table (%s) values (%s)' % (', '.join(kwarg.keys()), kwarg.values())).replace('[', '').replace(']', '')
        print 'ADD BUG -->> ', insert
        qr = self.db.cursor()
        qr.execute(insert)



    def add_bug_text(self, description = '', steps_to_reproduce = '', additional_information = ''):
        """
            Inserir bug on project
        """
        text = {}
        text['description'] = description
        text['steps_to_reproduce'] = steps_to_reproduce
        text['additional_information'] = additional_information

        insert = ('INSERT into mantis_bug_text_table (%s) values (%s)' % (', '.join(text.keys()), text.values())).replace('[', '').replace(']', '')
        print 'ADD TEXT -->> ', insert
        qr = self.db.cursor()
        qr.execute(insert)
        print 'LAST ID TEXT -->>' , self.db.insert_id()
        self.last_text_insert_id = int(self.db.insert_id())
        """ Add bug for text """
        self.bug(bug_text_id = self.db.insert_id())

        return True


if __name__ == '__main__':
    mantis = Mantis()
    mantis.add_bug_text(description = 'Test for report bug on Mantis')
