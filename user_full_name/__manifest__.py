# -*- coding: utf-8 -*-
{
    'name': "Deprecated Users Full Name",

    'summary': """Use user_full_name_mixin instead.
Users first and last names""",

    'description': """
                Users
    """,

    'author': "Maksym K",
    'website': "http://www.lumirang.com",
    'category': 'Users',
    'version': "13.0.1.0",
    'license': "Other proprietary",
    'depends': ['contacts'],
    'data': [
        'views/res_users.xml',
        'views/res_partner.xml',
    ],
    'sequence': 2,
    'application': True,
}
