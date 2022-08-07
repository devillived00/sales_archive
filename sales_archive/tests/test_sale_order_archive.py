from odoo.tests import TransactionCase
import datetime
from dateutil.relativedelta import relativedelta


class TestSaleOrderArchive(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """ Set up data before all test method."""
        super(TestSaleOrderArchive, cls).setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })

        cls.sale_order_1 = cls.env['sale.order'].create({
            'name': 'SO123',
            'partner_id': cls.partner.id,
            'state': 'sale',
        })
        cls.sale_order_2 = cls.env['sale.order'].create({
            'name': 'SO124',
            'partner_id': cls.partner.id,
            'state': 'sale',
        })
        cls.sale_order_3 = cls.env['sale.order'].create({
            'name': 'SO125',
            'partner_id': cls.partner.id,
            'state': 'cancel',
        })
        cls.sale_order_4 = cls.env['sale.order'].create({
            'name': 'SO126',
            'partner_id': cls.partner.id,
            'state': 'cancel',
        })
        cls.sale_order_5 = cls.env['sale.order'].create({
            'name': 'SO127',
            'partner_id': cls.partner.id,
            'state': 'draft',
        })

    def test_get_orders_to_archive_so_unlinked(self):
        """
        Test if correct Sale Orders are unlinked after the function execution.
        """
        
        # Returning order which should be unlinked
        sale_orders_to_archive = self.env['sale.order'].search( 
            [('id', 'in', [self.sale_order_1.id, self.sale_order_2.id, self.sale_order_3.id])])
        
        # Setting up write_date to be later than 30 days.
        for order in sale_orders_to_archive:
            order.write({
                'write_date': datetime.date.today() - relativedelta(days=35)
            })
        
        self.env['sale.order.archive'].get_orders_to_archive()
        
        # Returning order which should have been unlinked
        sale_orders_to_archive = self.env['sale.order'].search(
            [('id', 'in', [self.sale_order_1.id, self.sale_order_2.id, self.sale_order_3.id])])
        
        
        self.assertEqual(
            0,
            len(sale_orders_to_archive)
        )

    def test_get_orders_to_archive_soa_created(self):
        """
        Test if correct quantity of archived Sale Orders has been created.
        """
        
        # Returning order which should be archived
        sale_orders_to_archive = self.env['sale.order'].search( 
            [('id', 'in', [self.sale_order_1.id, self.sale_order_2.id, self.sale_order_3.id])])
        
        # Setting up write_date to be later than 30 days.
        for order in sale_orders_to_archive:
            order.write({
                'write_date': datetime.date.today() - relativedelta(days=35)
            })
        
        self.env['sale.order.archive'].get_orders_to_archive()
        
        archived_sale_orders = self.env['sale.order.archive'].search([('name', 'in', ['SO123','SO124','SO125'])])
        
        self.assertEqual(
            3, # Count of Sale Orders to archive
            len(archived_sale_orders)
        )