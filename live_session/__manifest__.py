{
    'name': "LiveSession",

    'summary': "LiveSession Integration",

    'description': "Add LiveSession JS code.",

    'author': "Artem Shelest",
    'website': "http://www.lumirang.com",
    'category': "Website",
    'version': "13.0.1.0",

    'depends': ['base_setup', 'web'],
    'data': [
        'views/assets.xml',
        'views/res_config_settings.xml',
    ],
    'sequence': 2,
    'application': True,
}
