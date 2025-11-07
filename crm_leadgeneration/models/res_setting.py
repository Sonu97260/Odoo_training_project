from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'res config settings'

    lead_num = fields.Boolean(
        string="Lead numbers & transfer",
        config_parameter='crm_leadgeneration.lead_num'
    )
    prefix = fields.Char(
        string="Prefix",
        config_parameter='crm_leadgeneration.prefix'
    )
    start_num = fields.Integer(
        string="Start Number",
        config_parameter='crm_leadgeneration.start_num'
    )

   
