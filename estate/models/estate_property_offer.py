from datetime import timedelta, datetime
from odoo import api, fields, models

class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy="false")
    partner_id = fields.Many2one("res.partner", required=False)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", store=True, inverse="_inverse_date_deadline")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today().date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = abs((record.date_deadline - datetime.today().date()).days)

