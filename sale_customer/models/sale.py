from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sales Order'

    delivery_info=fields.Char(string="delivery Info")
    delivery_status=fields.Char(string="delivery Status")

    
    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        _logger.info("Custom SO fields: %s", invoice_vals)
        invoice_vals.update({
            'delivery_info': self.delivery_info,
            'delivery_status': self.delivery_status,
        })
        return invoice_vals
    
    def action_done_email(self):
        print("sent email.......................")
        template_id = self.env.ref('sale_customer.action_done_mail_id')
        print("template_id----------------",template_id)
        for sale in self:
            print("action done.............",sale.state)
            if sale.state == 'draft':
                print("action done.............")
                # sale.write({'state':'sale'})
                if template_id:
                    print("\n iffffffffffffffffffffff")
                    template_id.send_mail(sale.id,force_send=True)
            
