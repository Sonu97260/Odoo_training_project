from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import base64
from io import BytesIO
import xlsxwriter

import logging
_logger = logging.getLogger(__name__)

class saleorder(models.Model):
    _inherit = 'sale.order'
    _description = 'sales Order'
    _order = 'date_order desc'

    state=fields.Selection(selection_add=[
    ('quotation_approved', 'Apporved Quotation')],tracking=True)

    def action_quotation_approve(self):
        for rec in self:
            print("qutation approved.........")
            rec.state = 'quotation_approved'

    @api.model
    def cron_approve_quotation(self):
        three_days_ago = datetime.now() - timedelta(days=3)
        orders = self.search([
            ('state', '=', 'sale'),
            ('date_order', '<=', three_days_ago)
        ])
        for order in orders:
            print("Automatically approving quotation for order............................:")
            order.state = 'quotation_approved'
            
    def order_apporved(self):
        for order in self:
            print("Order approved - sending email...")
            order.state = 'quotation_approved'
            template = self.env.ref('salemanagement.order_apporved_send_email_iddd', raise_if_not_found=False)
            if template:
                template.send_mail(order.id, force_send=True) 

    def order_report(self):
        report=self.env.ref('salemanagement.sale_order_report_pdf').read()[0]
        print("report....................")
        return report
    
    def send_email_confirmed(self):
        for order in self:
            print("Order approved - sending email...........")
            order.state = 'quotation_approved'
            template = self.env.ref('salemanagement.send_email_template', raise_if_not_found=False)
            if template:
                template.send_mail(order.id, force_send=True)

    def xls_report(self):
        self.ensure_one()
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Sale Order')

        bold = workbook.add_format({'bold': True})

        sheet.write(0, 0, 'Order', bold)
        sheet.write(0, 1, 'Customer', bold)
        sheet.write(0, 2, 'Amount Total', bold)

        row = 1
        for order in self:
            sheet.write(row, 0, order.name or '')
            sheet.write(row, 1, order.partner_id.name or '')
            sheet.write(row, 2, order.amount_total or 0)
            row += 1

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())

    
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.name}_report.xlsx',
            'type': 'binary',
            'datas': file_data,
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })    
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
