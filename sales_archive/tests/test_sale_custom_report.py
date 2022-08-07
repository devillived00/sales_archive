from odoo.tests import TransactionCase
 

class TestSaleCustomReport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """ Set up data before all test method."""
        super(TestSaleCustomReport, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })

        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
        })
        cls.product2 = cls.env['product.product'].create({
            'name': 'Test Product2',
        })
        cls.product3 = cls.env['product.product'].create({
            'name': 'Test Product3',
        })

        cls.sale_order_1 = cls.env['sale.order'].create({
            'name': 'SO123',
            'partner_id': cls.partner.id,
            'state': 'sale'
        })
        cls.sale_order_2 = cls.env['sale.order'].create({
            'name': 'SO124',
            'partner_id': cls.partner.id,
            'state': 'sale'
        })
        cls.sale_order_3 = cls.env['sale.order'].create({
            'name': 'SO125',
            'partner_id': cls.partner.id,
            'state': 'draft'
        })

        cls.sale_order_line1 = cls.env['sale.order.line'].create({
            'name': cls.product.name,
            'product_id': cls.product.id,
            'product_uom_qty': 2,
            'price_unit': 17,
            'order_id': cls.sale_order_1.id,
            'tax_id': False,

        })
        cls.sale_order_line2 = cls.env['sale.order.line'].create({
            'name': cls.product2.name,
            'product_id': cls.product2.id,
            'product_uom_qty': 2,
            'price_unit': 10,
            'order_id': cls.sale_order_2.id,
            'tax_id': False,
        })
        cls.sale_order_line3 = cls.env['sale.order.line'].create({
            'name': cls.product3.name,
            'product_id': cls.product3.id,
            'product_uom_qty': 2,
            'price_unit': 20,
            'order_id': cls.sale_order_1.id,
            'tax_id': False,
        })
        cls.sale_order_line4 = cls.env['sale.order.line'].create({
            'name': cls.product2.name,
            'product_id': cls.product2.id,
            'product_uom_qty': 2,
            'price_unit': 20,
            'order_id': cls.sale_order_3.id,
            'tax_id': False,
        })
        cls.sale_order_line5 = cls.env['sale.order.line'].create({
            'name': cls.product2.name,
            'product_id': cls.product2.id,
            'product_uom_qty': 2,
            'price_unit': 20,
            'order_id': cls.sale_order_1.id,
            'tax_id': False,
        })
        cls.sale_order_line5 = cls.env['sale.order.line'].create({
            'name': cls.product3.name,
            'product_id': cls.product3.id,
            'product_uom_qty': 3,
            'price_unit': 28,
            'order_id': cls.sale_order_2.id,
            'tax_id': False,
        })

        cls.orders_for_report = cls.env['sale.order'].search(
            [('id', 'in', [cls.sale_order_1.id, cls.sale_order_2.id])])

        cls.sale_custom_report = cls.env['sale.custom.report'].with_context(
            data=str(cls.orders_for_report)).create({})

    def test_get_sale_orders(self):
        """
        Test if function returns Sale Orders from context correctly.
        """

        self.assertEqual(
            self.orders_for_report,
            self.sale_custom_report.get_sale_orders()
        )

    def test_get_order_lines_ids(self):
        """
        Test if function returns correc Sale Order Lines
        """

        order_lines_ids = self.env['sale.order.line'].search(
            [('order_id', 'in', [self.sale_order_1.id, self.sale_order_2.id])]).ids

        self.assertEqual(
            order_lines_ids,
            self.sale_custom_report.get_order_lines_ids()
        )

    def test_get_product_list(self):
        """
        Test if function returns correct product list.
        """

        products = self.env['product.product'].search(
            [('id', 'in', [self.product.id, self.product2.id, self.product3.id])])
        products = [product for product in products]
        self.assertItemsEqual(
            products,
            self.sale_custom_report.get_product_list()
        )

    def test_get_product_order_count(self):
        """
        Test if fucntion returns correct Sale Oder count of given product.
        """
        
        self.assertEqual(
            1,  # product occurs in one confirmed sale order: sale_order_1
            self.sale_custom_report.get_product_order_count(self.product.id)
        )
        self.assertEqual(
            2,  # product2 occurs in two confirmed sale orders: sale_order_1, sale_order_2
            self.sale_custom_report.get_product_order_count(self.product2.id)
        )
        self.assertEqual(
            2,  # product3 occurs in two confirmed sale orders: sale_order_1, sale_order_2
            self.sale_custom_report.get_product_order_count(self.product3.id)
        )

    def test_get_average_price(self):
        """
        Test if fucntion returns correct average price of given product.
        """
        
        self.assertEqual(
            17,  # product prices: 17, 17 avg: 17
            self.sale_custom_report.get_average_price(self.product.id)
        )
        self.assertEqual(
            15,  # product2 prices: 10, 10, 20, 20, avg: 15
            self.sale_custom_report.get_average_price(self.product2.id)
        )
        self.assertEqual(
            24.8,  # product3 prices: 20, 20, 28 ,28, 28 avg: 24.8
            self.sale_custom_report.get_average_price(self.product3.id)
        )

    def test_get_total_amount(self):
        """
        Test if function returns correct total sale value of given product.
        """
        
        self.assertEqual(
            34,  # product prices: 17, 17 sum: 34
            self.sale_custom_report.get_total_amount(self.product.id)
        )
        self.assertEqual(
            60,  # product2 prices: 10, 10, 20, 20, sum: 60
            self.sale_custom_report.get_total_amount(self.product2.id)
        )
        self.assertEqual(
            124,  # product3 prices: 20, 20, 28 ,28, 28 sum: 124
            self.sale_custom_report.get_total_amount(self.product3.id)
        )

    def test_action_generate_report(self):
        """
        Test if function returns correct view.
        """
        
        expected_values = {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.sale_custom_report.id,
            'res_model': self.sale_custom_report._name,
            'target': 'new',
            'context': {
                    'default_model': self.sale_custom_report._name,
            },
        }

        self.assertEqual(
            expected_values,
            self.sale_custom_report.action_generate_report()
        )
