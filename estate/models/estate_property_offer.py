from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")], copy="false")
    partner_id = fields.Many2one("res.partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", store=True, inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today().date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = abs((record.date_deadline - datetime.today().date()).days)

    def action_accept(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(_("This offer has already been accepted"))

            property_offers = self.env["estate.property.offer"].search(
                [("property_id", "=", record.property_id.id), ("status", "=", "accepted")]
            )

            if property_offers:
                raise UserError(_("This property already has an accepted offer"))

            record.property_id.write(
                {
                    "buyer_id": record.partner_id.id,
                    "selling_price": record.price,
                    "state": "offer_accepted",
                }
            )
            record.status = "accepted"
        return True

    def action_cancel(self):
        for record in self:
            record.status = "refused"
        return True

    @api.model
    def create(self, vals):
        property = self.env["estate.property"].browse(vals["property_id"])

        if property.state == "sold":
            raise UserError(_("Cannot create an offer for a sold property"))

        offers = property.offer_ids
        max_offer = max(offers.mapped("price"), default=0)
        if vals["price"] <= max_offer:
            raise UserError(_("The offer must be greater than ") + str(max_offer))
        property.state = "offer_received"
        return super().create(vals)

    def find_accepted_offer(self):
        return self.property_id.offer_ids.filtered(lambda element: element.status == "accepted")
