from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'crm lead'

    lead_num = fields.Char(string="Lead Number", readonly=True,copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        config = self.env['ir.config_parameter'].sudo()

        lead_num = config.get_param("crm_leadgeneration.lead_num") == "True"
        prefix = config.get_param("crm_leadgeneration.prefix", "LEAD")

        # Get and clean current number
        current_num = config.get_param("crm_leadgeneration.current_num", "1")
        current_num_str = str(current_num).strip()

        # If value is NOT numeric → reset to 1
        if not current_num_str.isdigit():
            current_num_str = "1"
            config.set_param("crm_leadgeneration.current_num", current_num_str)

        for vals in vals_list:

            if lead_num:

                # Generate number
                sequence = f"{prefix}/{current_num_str}"
                vals["lead_num"] = sequence
                vals["name"] = sequence

                # Increase number
                next_num_int = int(current_num_str) + 1

                # Zero-pad to same length
                next_num_str = str(next_num_int).zfill(len(current_num_str))

                # Save to config
                config.set_param("crm_leadgeneration.current_num", next_num_str)

                # Update for next loop
                current_num_str = next_num_str

        return super().create(vals_list)


    # @api.model_create_multi
    # def create(self, vals_list):
    #     config = self.env['ir.config_parameter'].sudo()

    #     lead_num = config.get_param("crm_leadgeneration.lead_num") == "True"
    #     prefix = config.get_param("crm_leadgeneration.prefix", "LEAD")

        
    #     current_num = config.get_param("crm_leadgeneration.current_num")
    #     current_num_str = str(current_num)

    #     for vals in vals_list:

    #         if lead_num:

    #             sequence = f"{prefix}/{current_num_str}"

    #             vals["lead_num"] = sequence
    #             vals["name"] = sequence

    #             next_num_int = int(current_num_str) + 1
               
    #             next_num_str = str(next_num_int).zfill(len(current_num_str))

                
    #             config.set_param("crm_leadgeneration.current_num", next_num_str)

    #             current_num_str = next_num_str

    #     return super(CrmLead, self).create(vals_list)

    def action_open_transfer_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_ids': self.ids}

    }

    

    
    
    