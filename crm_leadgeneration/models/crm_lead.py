from odoo import api, fields, models,_
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from lxml import etree

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _description = 'crm lead'

    show_button = fields.Boolean(
        string="Show Transfer Button",
        compute="_compute_show_button",
        store=False,
    )
    lead_num = fields.Char(
        string="Lead Number",
        readonly=True,
        copy=False
    )

    # -------------------------------------------------------------------------
    # COMPUTE FIELD
    # -------------------------------------------------------------------------
    @api.depends_context('uid')
    def _compute_show_button(self):
        """
        Compute if the transfer button should be shown based on system parameter.
        This reads from Settings configuration.
        """
        config = self.env['ir.config_parameter'].sudo()
        show_button_param = config.get_param(
            'crm_leadgeneration.show_lead_transfer_button',
            'True'
        )
        show_button = show_button_param == 'True'
        
        for lead in self:
            lead.show_button = show_button
            _logger.info(
                f"Computing show_button for Lead {lead.id} | "
                f"show_button={show_button}"
            )

    # -------------------------------------------------------------------------
    # CREATE - Adds lead numbering logic
    # -------------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to add automatic lead numbering.
        """
        config = self.env['ir.config_parameter'].sudo()

        for vals in vals_list:
            # Get lead numbering configuration
            lead_num_enabled = config.get_param(
                'crm_leadgeneration.lead_num'
            ) == 'True'
            prefix = config.get_param('crm_leadgeneration.prefix', 'LEAD')
            start_num = int(config.get_param(
                'crm_leadgeneration.start_num',
                1
            ))
            current_num = int(config.get_param(
                'crm_leadgeneration.current_num',
                start_num
            ))
            digit_length = int(config.get_param(
                'crm_leadgeneration.digit_length',
                1
            ))

            # Ensure current_num is not less than start_num
            if current_num < start_num:
                current_num = start_num
                config.set_param('crm_leadgeneration.current_num', start_num)

            # Generate lead number if enabled
            if lead_num_enabled:
                if digit_length > 0:
                    sequence = f"{prefix}{str(current_num).zfill(digit_length)}"
                else:
                    sequence = f"{prefix}{current_num}"

                vals['lead_num'] = sequence
                vals['name'] = sequence
                
                # Increment counter
                config.set_param(
                    'crm_leadgeneration.current_num',
                    current_num + 1
                )
                
                _logger.info(f"Created lead with number: {sequence}")

        leads = super(CrmLead, self).create(vals_list)
        return leads

    # -------------------------------------------------------------------------
    # ACTION - Open transfer wizard
    # -------------------------------------------------------------------------
    def action_open_transfer_wizard(self):
        """
        Opens a popup window for transferring leads.
        This is called when the Transfer Lead button is clicked.
        """
        _logger.info(f"Opening Transfer Wizard for Leads: {self.ids}")

        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer Leads',
            'res_model': 'crm.lead.transfer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_lead_ids': self.ids,
                'active_ids': self.ids,
                'active_model': 'crm.lead',
            },
        }


    # show_button = fields.Boolean(string="Show Transfer Button", compute="_compute_show_button", store=False )
    # lead_num = fields.Char(string="Lead Number", readonly=True, copy=False)


    # @api.model
    # def default_get(self, fields_list):
    #     print()
    #     res = super().default_get(fields_list)
    #     show_button = True
       
    #     if self.show_button:
    #         print("show ifff..........",show_button)
    #         show_button = True
    #     else:
    #         show_button = False    
            
    #     res['__context'] = dict(self.env.context, hide_transfer_button=show_button)
    #     return res

    # # def _compute_show_button(self):
    # #     enabled = self.env['ir.config_parameter'].sudo().get_param('crm_leadgeneration.lead_num') == 'True'
    # #     for lead in self:
    # #         lead.show_button = enabled

    # @api.depends_context('hide_transfer_button')
    # def _compute_show_button(self):
    #     print("\n _compute_show_button------------")
    #     for lead in self:
    #         hide_ctx = self.env.context.get('hide_transfer_button', False)
    #         print("\n hide_ctx---",hide_ctx)
    #         lead.show_button = not hide_ctx 


    # @api.model_create_multi
    # def create(self, vals):
    #     config = self.env['ir.config_parameter'].sudo()

    #     lead_num = config.get_param('crm_leadgeneration.lead_num') == 'True'
    #     prefix = config.get_param('crm_leadgeneration.prefix', 'LEAD')
    #     start_num = int(config.get_param('crm_leadgeneration.start_num', 1))
    #     current_num = int(config.get_param('crm_leadgeneration.current_num', start_num))
    #     digit_length = int(config.get_param('crm_leadgeneration.digit_length', 1))

    #     if current_num < start_num:
    #         current_num = start_num
    #         config.set_param('crm_leadgeneration.current_num', start_num)

    #     if lead_num:
          
    #         if digit_length > 0:
    #             sequence = f"{prefix}{str(current_num).zfill(digit_length)}"
    #         else:
    #             sequence = f"{prefix}{current_num}"

    #         vals['lead_num'] = sequence
    #         vals['name'] = sequence
    #         config.set_param('crm_leadgeneration.current_num', current_num + 1)

    #     return super(CrmLead, self).create(vals)


    # def action_open_transfer_wizard(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'crm.lead.transfer.wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {'active_ids': self.ids}

    #     }
    
    
    