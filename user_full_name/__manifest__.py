# -*- coding: utf-8 -*-
{
    'name': "Users Full Name",

    'summary': """
        Users first and last names""",

    'description': """
                Users
    """,

    'author': "Maksym K",
    'website': "http://www.lumirang.com",
    'category': 'Users',
    'version': '0.1',

    'depends':  ['contacts'],
    'data': [
        'views/res_users.xml',
        'views/res_partner.xml',
        ],
    'sequence': 2,
    'application': True,
}
