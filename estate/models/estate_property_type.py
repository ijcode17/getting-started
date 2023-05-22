from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type Model"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer()
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [("unique_name", "UNIQUE(name)", "The name of the property type must be unique")]

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_view_offers(self):
        self.ensure_one()
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "estate.property.offer",
            "domain": [("property_type_id", "=", self.id)],
            "context": "{'create': False}",
        }
