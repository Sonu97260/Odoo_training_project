from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class LeadTransferWizard(models.TransientModel):
    _name = 'crm.lead.transfer.wizard'
    _description = 'CRM Lead Transfer Wizard'

    assigned_id = fields.Many2one('res.users', string='Assigned', readonly=True)
    assign_to_id = fields.Many2one('res.users', string='Assign To', required=True)


    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids')
        if active_ids:
            lead = self.env['crm.lead'].browse(active_ids[0])
            res['assigned_id'] = lead.user_id.id
        return res
    
    def action_confirm_transfer(self):
        active_ids = self.env.context.get('active_ids')
        leads = self.env['crm.lead'].browse(active_ids)
        for lead in leads:
            lead.sudo().write({'user_id': self.assign_to_id.id})
        return {'type': 'ir.actions.act_window_close'}

    