from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import date

from odoo import api, fields, models

class InvoiceOrder(models.Model):
    _inherit = 'account.move'
    _description = 'Invoice Order'

    delivery_info = fields.Char(string="Delivery Info")
    delivery_status = fields.Char(string="Delivery Status")
    x_nature_operation = fields.Char(string="Nature of Operation")

    penalty_amount = fields.Monetary(
        string="Penalty Amount",
        compute="_compute_amount",
        currency_field='currency_id',
        store=True
        )
    
    def action_quotation_send(self):
        print("sending action done...............")
        

    @api.depends('line_ids.price_subtotal', 'penalty_amount', 'invoice_date_due')
    def _compute_amount(self):
        print("Hello from invoice//////////////////////")
        super()._compute_amount()
        today = fields.Date.today()
        for move in self:
            penalty = 0.0
            if move.invoice_date_due and move.amount_total > 0:
                days_overdue = (today - move.invoice_date_due).days
                if days_overdue > 0:
                    penalty = (move.amount_total * 0.05) * days_overdue

        move.penalty_amount = move.currency_id.round(penalty)
        #add
        # move.amount_total = move.currency_id.round(move.amount_total + penalty)
        move.amount_total = 777
        move.amount_residual = move.currency_id.round(move.amount_residual + penalty)
        
