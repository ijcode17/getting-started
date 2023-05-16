from odoo import api, fields, models

class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy="false")
    partner_id = fields.Many2one("res.partner", required=False)
    property_id = fields.Many2one("estate.property", required=True)

    