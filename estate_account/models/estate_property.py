from odoo import Command, models
import logging


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        logging.info(" reached ".center(100, "="))

        self = self.sudo()

        self.check_access_rights("write")
        self.check_access_rule("write")

        accepted_offer = self.offer_ids.find_accepted_offer()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        self.env["account.move"].create(
            {
                "partner_id": accepted_offer.partner_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.name,
                            "quantity": 1,
                            "price_unit": self.selling_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Administrative Fees",
                            "quantity": 1,
                            "price_unit": 100.0,
                        }
                    ),
                    Command.create(
                        {
                            "name": "Sales Commission",
                            "quantity": 1,
                            "price_unit": self.selling_price * 0.06,
                        }
                    ),
                ],
            }
        )
        res = super().action_sold()
        print("Executing action_sold() from estate_account")
        return res
