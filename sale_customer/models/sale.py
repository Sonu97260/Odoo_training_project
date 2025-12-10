from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

# class saleorder(models.Model):
#     _inherit = 'sale.order'
#     _description = 'sales Order'

#     attachment_file = fields.Binary("Attachment")
#     attachment_filename = fields.Char("Filename")


#     # state = fields.Selection(selection_add=[('quotation_approved', "Quotation Approved")],tracking=True)

#     # def action_quotation_approve(self):
#     #     for rec in self:
#     #         rec.state = 'quotation_approved'


#     delivery_info=fields.Char(string="delivery Info")
#     delivery_status=fields.Char(string="delivery Status")
   
#     # # @api.model
#     # def create(self, vals):
#     #     print("=====================sequenc change///////////////")
#     #     if vals.get('name', 'New') == 'New':
#     #         seq = self.env['ir.sequence'].next_by_code('sale.order') or '/'
#     #         vals['name'] = seq.replace("S", "SO-2025-")  
        
#     #     return super(SaleOrder, self).create(vals)
    
#     # @api.model
#     # def create(self, vals):
#     #     record = super(saleorder, self).create(vals)
#     #     print("\n records-------------------")
#     #     print(">>> Custom create called with vals:", vals)
#     #     if vals.get('name', 'New') == 'New':
#     #         seq = self.env['ir.sequence'].next_by_code('sale.order.sequence') or '/'
#     #         vals['name'] = seq.replace("S", "SO-2025-", 1)
#     #     return record       
    
#     # def write(self, vals):
#     #     print("deliver info .........")
#     #     vals['delivery_info'] = "Will deliver in 2 days"
#     #     return super(saleorder, self).write(vals)   
     
#     def _prepare_invoice(self):
#         invoice_vals = super()._prepare_invoice()
#         _logger.info("Custom SO fields: %s", invoice_vals)
#         invoice_vals.update({
#             'delivery_info': self.delivery_info,
#             'delivery_status': self.delivery_status,
#         })
#         return invoice_vals

    
#     def action_done_email(self):
#         print("sent email.......................")
#         template_id = self.env.ref('sale_customer.action_done_mail_id')
#         print("template_id----------------",template_id)
#         for sale in self:
#             print("action done.............",sale.state)
#             if sale.state == 'draft':
#                 print("action done.............")
#                 if template_id:
#                     template_id.send_mail(sale.id,force_send=True)
        
#     # def create(self, vals):
#     #     vals=super()._create()
#     #     print("sequence change...............")
#     #     if vals.get('name', _('New')) == _('New'):
#     #        vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.sequence')
#     #     return True
    


class saleorder(models.Model):
    _inherit = 'sale.order.line'
    _description = 'sales Order Line'

    # attachment_file = fields.Binary("Attachment")
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'sale_line_ir_attachment_rel',
        'sale_line_id',
        'attachment_id',
        string="Attachments"
)

    def action_preview_attachment(self):
        self.ensure_one()
        if not self.attachment_ids:
            return
        attachment = self.attachment_ids[0]  # preview first attachment
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=false',
            'target': 'new',
        }


   

    


     
   