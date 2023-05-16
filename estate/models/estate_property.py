from datetime import datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstatePropertyModel(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property Model'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, copy=False, default='new')
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price", store=True, default=0.0)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'El precio esperado debe ser positivo'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'El precio de venta debe ser positivo'),
        ('unique_name', 'UNIQUE(property_type_id , name)', 'El nombre de la propiedad debe ser único'),
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
          if record.offer_ids:
            record.best_price = max(record.offer_ids.mapped('price'))
          else:
            record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if record.state == 'canceled':
              continue

            if record.state == 'sold':
              raise UserError("No se puede cancelar una propiedad vendida")


            record.state = 'canceled'
        return True
    
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
              raise UserError("No se puede vender una propiedad cancelada")

            if record.state == 'sold':
              continue

            record.state = 'sold'
        return True
    
    @api.constrains('offer_ids.price')
    def _check_offer_price(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.price <= 0:
                    raise ValidationError('El precio de la oferta debe ser estrictamente positivo.')

    @api.onchange('expected_price', 'selling_price')
    def _onchange_price(self):
        if not float_is_zero(self.selling_price, precision_digits=2) and float_compare(self.selling_price, self.expected_price * 0.9, precision_digits=2) == -1:
            self.selling_price = self.expected_price * 0.9

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError('El precio de venta no puede ser inferior al 90% del precio esperado.')
            
