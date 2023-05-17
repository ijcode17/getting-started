from datetime import timedelta, datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
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

    def action_accept(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(_("This offer has already been accepted"))
            
            property_offers = self.env['estate.property.offer'].search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])

            if property_offers: 
                raise UserError(_("This property already has an accepted offer"))

            record.property_id.buyer_id = record.partner_id.id
            record.property_id.selling_price = record.price
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
        return True
    
    def action_cancel(self):
        for record in self:
            record.status = 'refused'
        return True
    
