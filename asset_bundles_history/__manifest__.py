{
    'name': "Asset Bundles History",
    'summary': "More control over asset bundles lifecycle",
    'description': "Retain asset bundles",

    'author': "Artem Shelest",
    'website': "https://lumirang.com",
    'category': "Tools",
    'version': "13.0.1.0",

    'depends': ['base'],
    'data': [
        'views/obsolete_asset_bundle.xml',
        'security/ir.model.access.csv',
    ],
    'sequence': 2,
    'application': True,
}
