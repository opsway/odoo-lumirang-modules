{
    'name': "Force Timezone",

    'summary': "Set server-wide users' timezone",

    'description': "Restrict all users to a selected timezone.",

    'author': "Artem Shelest",
    'website': "http://www.lumirang.com",
    'category': "Core",
    'version': "13.0.1.0.0",
    'license': "Other proprietary",
    'depends': ["web"],
    'data': [
        "views/assets.xml",
        "views/res_users_views.xml",
        "views/res_config_settings_views.xml",
    ],
    'sequence': 2,
    'application': False,
}
