{
    'name': 'My first module',
    'summary': 'Real estate module of the technical course getting started with odoo',
    'version': '16.0.1.0.0',
    'author': 'Vauxoo',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
    ],
    "application": True,
}

