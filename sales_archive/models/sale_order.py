from odoo import models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_open_report_wizard(self):
        """
        Function provides data and opens wizard view. Accepts only confirmed Sale Orders. 

        Raises:
            ValidationError: Raises ValidationError when user tries to use this function on Orders with states different than 'sale'.

        Returns:
            wizard: Wizard view in which we can generate special report of choosen Sale Orders.
        """
        
        for record in self:
            if record.state != "sale":
                raise ValidationError(f"Report can be created only from posted Sale Orders! To proceed please confirm order: {record.name}.")
        
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'sale.custom.report',
            'target': 'new',
            'context': {
                'data': self
            },
                    }