from odoo import fields, models,api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_lead_transfer_button = fields.Boolean(
        string="Show Lead Transfer Button",
        config_parameter='crm_leadgeneration.show_lead_transfer_button',
        default=True,
        help="Enable this to show the Transfer Lead button in CRM Lead list view. "
             "When disabled, the button will be hidden from all users."
    )

    lead_num = fields.Boolean("Enable Lead Number", config_parameter='crm_leadgeneration.lead_num') 
    prefix = fields.Char("Prefix", default="LEAD", config_parameter='crm_leadgeneration.prefix') 
    start_num = fields.Integer("Start Number", default=1, config_parameter='crm_leadgeneration.start_num') 
    current_num = fields.Integer(string="Current Number",config_parameter='crm_leadgeneration.current_num', readonly=True)
    digit_length = fields.Integer(string="Digit Length", config_parameter='crm_leadgeneration.digit_length',default=1)


    @api.model
    def get_values(self):
        res = super().get_values()
        config = self.env['ir.config_parameter'].sudo() 
        res.update( lead_num=config.get_param('crm_leadgeneration.lead_num') == 'True', 
        prefix=config.get_param('crm_leadgeneration.prefix', 'LEAD'),
        start_num=int(config.get_param('crm_leadgeneration.start_num', 1)), 
        current_num=int(config.get_param('crm_leadgeneration.current_num', 1)), 
        digit_length=int(config.get_param('crm_leadgeneration.digit_length', 1)), ) 
        return res

    
    def set_values(self): 
        super().set_values() 
        config = self.env['ir.config_parameter'].sudo() 
        config.set_param('crm_leadgeneration.lead_num', self.lead_num) 
        config.set_param('crm_leadgeneration.prefix', self.prefix) 
        config.set_param('crm_leadgeneration.start_num', self.start_num) 
        config.set_param('crm_leadgeneration.digit_length', self.digit_length) 
        current_num = int(config.get_param('crm_leadgeneration.current_num', self.start_num)) 
        if self.start_num > current_num or self.start_num != current_num: 
            config.set_param('crm_leadgeneration.current_num', self.start_num)

