from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"


    lead_num = fields.Boolean(
        "Enable Lead Number",
        config_parameter="crm_leadgeneration.lead_num"
    )
    prefix = fields.Char(
        "Prefix",
        default="LEAD",
        config_parameter="crm_leadgeneration.prefix"
    )
    start_num = fields.Char(
        "Start Number",
        default=1,
        config_parameter="crm_leadgeneration.start_num"
    )
    current_num= fields.Char(
        "Current Number",
        readonly=True,
        config_parameter="crm_leadgeneration.current_num"
    )
    digit_length = fields.Integer(
    "Digit Length",
    default=5,                 # FIXED
    config_parameter="crm_leadgeneration.digit_length",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        config = self.env['ir.config_parameter'].sudo()

        res.update(
            lead_num=config.get_param("crm_leadgeneration.lead_num") == "True",
            prefix=config.get_param("crm_leadgeneration.prefix", "LEAD"),
            start_num=config.get_param("crm_leadgeneration.start_num", "1"),
            current_num=config.get_param("crm_leadgeneration.current_num", "1"),
            digit_length=int(config.get_param("crm_leadgeneration.digit_length", 1)),
        )
        return res

    def set_values(self):
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()

        config.set_param("crm_leadgeneration.lead_num", self.lead_num)
        config.set_param("crm_leadgeneration.prefix", self.prefix)

        # EXACT start number with leading zeros preserved
        raw_start = str(self.start_num)
        config.set_param("crm_leadgeneration.start_num", raw_start)

        # Reset current number to EXACT start number
        config.set_param("crm_leadgeneration.current_num", raw_start)

        # Save digit length for increment formatting
        config.set_param("crm_leadgeneration.digit_length", self.digit_length)


 


