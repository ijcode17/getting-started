{
    "name": "My first module",
    "summary": "Real estate module of the technical course getting started with odoo",
    "version": "16.0.1.0.0",
    "author": "Vauxoo",
    "category": "Real Estate/Brokerage",
    "depends": [
        "base",
    ],
    "data": [
        "data/estate.property.type.csv",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_offer_views.xml",
        "views/res_users_views.xml",
        "views/estate_menus.xml",
    ],
    "demo": [
        "demo/estate_property.xml",
    ],
    "application": True,
    "installable": True,
}
