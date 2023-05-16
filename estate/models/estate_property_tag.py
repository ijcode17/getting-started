from odoo import fields, models

class EstatePropertyTagModel(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag Model"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', "El nombre de la etiqueta debe ser único")    
    ]
    
