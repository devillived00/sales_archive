from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestSaleOrderArchive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """ Set up data before all test method."""
        super(TestSaleOrderArchive, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })

        cls.correct_order_1 = cls.env['sale.order'].create({
            'name': 'SO123',
            'partner_id': cls.partner.id,
            'state': 'sale',
        })
        cls.correct_order_2 = cls.env['sale.order'].create({
            'name': 'SO124',
            'partner_id': cls.partner.id,
            'state': 'sale',
        })
        cls.incorrect_order = cls.env['sale.order'].create({
            'name': 'SO125',
            'partner_id': cls.partner.id,
            'state': 'cancel',
        })

    def test_action_open_record_wizard_error(self):
        """
        Test if error is raised if any Sale Order is in 'cancel' state.
        """
        incorrect_orders = self.env['sale.order'].search(
            [('id', 'in', [self.correct_order_1.id, self.correct_order_2.id, self.incorrect_order.id])])

        with self.assertRaises(ValidationError):
            incorrect_orders.action_open_report_wizard()

    def test_action_open_record_wizard(self):
        """
        Test if function returns correct values.
        """

        correct_orders = self.env['sale.order'].search(
            [('id', 'in', [self.correct_order_1.id, self.correct_order_2.id])])

        expected_values = {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'sale.custom.report',
            'target': 'new',
            'context': {
                'data': correct_orders
            },
        }

        self.assertEqual(
            expected_values,
            correct_orders.action_open_report_wizard()
        )
