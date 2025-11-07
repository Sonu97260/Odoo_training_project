from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'crm lead'



    def action_generate_lead_number(self):
        """Example button action on list view"""
        for lead in self:
            if not lead.lead_num:
                lead.lead_num = self.env['ir.sequence'].next_by_code('crm.lead.custom')
        return True
    

    @api.model
    def create(self, vals):
        if self.env['ir.config_parameter'].sudo().get_param('crm_leadgeneration.lead_num') == 'True':
            prefix = self.env['ir.config_parameter'].sudo().get_param('crm_leadgeneration.prefix', 'LEAD')
            sequence = self.env['ir.sequence'].next_by_code('crm.lead.custom')
            if sequence:
                vals['name'] = sequence
            else:
                start = self.env['ir.config_parameter'].sudo().get_param('crm_leadgeneration.start_num', 1)
                vals['name'] = f"{prefix}{int(start):04d}"
        return super(CrmLead, self).create(vals)
    




