{
    'name': "JS Errors Log",
    'summary': "Save Javascript errors to the backend",
    'sequence': 15,
    'version': "13.0.1.0",
    'category': "Reporting",
    'website': "",
    'author': "Artem Shelest",
    'maintainer': "",
    'application': True,
    'installable': True,
    'auto_install': False,
    'depends': ['base', 'web'],
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'views/js_error.xml',
    ],
}
