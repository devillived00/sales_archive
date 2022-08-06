from odoo import fields, models
import datetime

class SaleOrderArchive(models.Model):
    _name = "sale.order.archive"
    
    name = fields.Char(string='Name')
    order_create_date = fields.Date(string='Date')
    customer = fields.Many2one('res.partner', string='Customer')
    saleperson = fields.Many2one('res.users', string='Saleperson')
    currency_id = fields.Many2one('res.currency', string="Currency")
    order_total_amount = fields.Monetary(string='Order Total Amount', readonly=True)
    order_lines_count = fields.Integer(string="Order Lines Count")
    
  
    def get_orders_to_archive(self):
        """
        Function gathers Sale Orders in state 'sale' or 'cancel and checks if any of them was last modified more than 30 days ago.
        For Sale Orders last modified later than 30 days ago, new SaleOrderArchive is created and then SaleOrder is being removed.
        """
        orders = self.env['sale.order'].search([('state', 'in', ['sale', 'cancel'])])
        
        for order in orders:
            if (datetime.date.today() - order.write_date.date()).days > 30:
                self.create({
                    'name': order.name,
                    'order_create_date': order.date_order,
                    'customer': order.partner_id.id,
                    'saleperson': order.user_id.id,
                    'currency_id': order.currency_id.id,
                    'order_total_amount': order.amount_total,
                    'order_lines_count': len(order.order_line)
                })
                if order.state == "sale":
                    order.action_cancel()
                order.unlink()
    