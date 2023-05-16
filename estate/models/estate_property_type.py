from odoo import fields, models

class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type Model"

    name = fields.Char(required=True)
    
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', "El nombre del tipo de propiedad debe ser único")
    ]

    