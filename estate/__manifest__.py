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
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml',
    ],
    "application": True,
}

