import base64
from odoo import fields, models
from odoo.tools import config
import csv
from datetime import datetime
import re


class SaleCustmoReport(models.TransientModel):
    _name = "sale.custom.report"
    _description = "SaleCustomReport"

    generated_csv = fields.Binary("CSV Report", readonly=True)
    csv_name = fields.Char("CSV Report Name", readonly=True)

    def get_sale_orders(self):
        """
        Returns:
            List of Sale Order objects, created from context data.
        """

        sale_orders_ids = self.env.context.get('data')
        sale_orders_ids = re.findall('\d+', sale_orders_ids)
        sale_orders_ids = map(int, sale_orders_ids)
        sale_orders = self.env['sale.order'].search(
            [('id', 'in', list(sale_orders_ids))])

        return sale_orders

    def get_order_lines_ids(self):
        """
        Returns:
            list: List of Sale Order Lines ids.
        """

        order_lines = [order.order_line for order in self.get_sale_orders()]
        order_lines_ids = [line.ids for line in order_lines]
        order_lines_ids = sum(order_lines_ids, [])

        return order_lines_ids

    def get_product_list(self):
        """
        Returns:
            list: List of product objects from Sale Order Lines without duplicates.
        """

        order_lines = [order.order_line for order in self.get_sale_orders()]
        product_list = [[line.product_id for line in line]
                        for line in order_lines]
        product_list = sum(product_list, [])
        product_list = list(set(product_list))

        return product_list

    def get_product_order_count(self, product_id):
        """
        Args:
            product_id (int): Product ID

        Returns:
            int: Quantity of Sale Orders with given product.
        """

        order_count = self.env['sale.order.line'].search(
            [('id', 'in', self.get_order_lines_ids()), ('product_id', '=', product_id)]).order_id

        return len(order_count)

    def get_average_price(self, product_id):
        """
        Args:
            product_id (int): Product ID

        Returns:
            float: Average price of given product.
        """

        lines = self.env['sale.order.line'].search(
            [('id', 'in', self.get_order_lines_ids()), ('product_id', '=', product_id)])

        prices = [line.price_subtotal for line in lines]
        quantities = [line.product_uom_qty for line in lines]

        average_unit_price = sum(prices) / sum(quantities)

        return round(average_unit_price, 2)

    def get_total_amount(self, product_id):
        """
        Args:
            product_id (int): Product ID

        Returns:
            float: Sales value of a given product.
        """
        
        lines = self.env['sale.order.line'].search(
            [('id', 'in', self.get_order_lines_ids()), ('product_id', '=', product_id)])

        amounts = [line.price_subtotal for line in lines]

        total_amount = sum(amounts)

        return total_amount

    def action_generate_report(self):
        """
        Generates CSV file with Sale Report from choosen Sale Orders. Sale report contains data like: Product, 
        Count of orders with the Product, Average product price and Sales value of the product.
        """
        
        data_dir = config['data_dir']

        with open(data_dir + '/sale_report.csv', mode='w', newline='') as file:
            report = csv.writer(file)
            report.writerow(["Product", "Order Count",
                            "Average Price", "Sale Amount"])
            for product in self.get_product_list():
                report.writerow(
                    [product.name, self.get_product_order_count(product.id), self.get_average_price(product.id), self.get_total_amount(product.id)])

        with open(data_dir + '/sale_report.csv', mode='r', newline='') as file:
            data = file.read()

        csv_bytes = data.encode()
        csv_bytes = base64.encodebytes(csv_bytes)

        self.write(
            {
                'generated_csv': csv_bytes,
                'csv_name': f"sale_report_{datetime.now().strftime('%Y-%m-%d')}.csv"
            }
        )

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'res_model': self._name,
            'target': 'new',
            'context': {
                    'default_model': self._name,
            },
        }
