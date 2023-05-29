from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.testt.common import TransactionCase


@tagged("post_install", "-at_install")
class EstatePropertyTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.properties = cls.env["estate.property"].create(
            {
                "name": "Big Villa",
                "property_type_id": "1",
                "state": "new",
                "description": "A nice and big villa",
                "postcode": "12345",
                "date_availability": "2020-02-02",
                "expected_price": "1600000",
                "bedrooms": "6",
                "living_area": "100",
                "facades": "4",
                "garage": "True",
                "garden": "True",
                "garden_area": "100000",
                "garden_orientation": "south",
                "salesman_id": cls.env.ref("base.user_admin").id,
            }
        )

    def test_action_sold(self):
        self.env["property.offer"].create(
            {
                "property_id": self.property.id,
                "partner_id": self.env.ref("base.res_partner_17").id,
                "status": "accepted",
                "price": 77000,
            }
        )
        self.property.action_sold()
        self.assertEqual(self.property.state, "sold")

        self.property.offer_ids.unlink()
        with self.assertRaises(UserError):
            self.property.action_sold()

        self.assertEqual(self.properties.state, "offer_received")

    def test_onchange_garden(self):
        self.property.onchange_garden()
        self.assertEqual(self.property.garden_area, 0)
        self.assertEqual(self.property.garden_orientation, "north")
