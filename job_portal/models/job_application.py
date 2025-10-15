from odoo import models, fields,api# type: ignore
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError # type: ignore
from datetime import date,timedelta
import logging


class JobApplication(models.Model):
    _name = "job.application"
    _description = "Job Application"
    _inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True)
    email = fields.Char(string="Email", store=True, required=True)
    phone = fields.Char(string="Phone")
    cv_attachment = fields.Binary(
        string="CV Attachment", attachment=True, help="Upload the CV here"
    )
    job_id = fields.Many2one("job.position", string="Job Position", required=True)
    
    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected'),
            ('hired', 'Hired')
        ],
        string='Status',
        default='draft',
        tracking=True
    )

    email_domain = fields.Char(string="Email Domain")

    # SQL constraints only
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'name must be unique!'),
        # ('check_email','check(age>=18)','age must be 18 above'),
        ]

    def send_approval_email(self):
        self.ensure_one()
        template = self.env.ref('job_portal.job_application_approval_email_template', raise_if_not_found=False)
        print("approval job ----------------", template)
        if template:
            template.send_mail(self.id, force_send=True)
        return True
    
    def action_shortlisted(self):
        self.write({'status': 'shortlisted'})
        template = self.env.ref('job_portal.job_application_shortlisted_email_template', raise_if_not_found=False)
        print("shortlisted job-----------", template)
        if template:
            for rec in self:
                return True
            
    def action_submitted(self):
        for rec in self:
            rec.status = 'submitted'

    def action_shortlisted(self):
        for rec in self:
            rec.status = 'shortlisted'

    def action_reject(self):
        for rec in self:
            rec.status = 'rejected'

    def action_hire(self):
        for rec in self:
            rec.status = 'hired'

    @api.onchange('email')
    def _onchange_email(self):
        if self.email:
            parts = self.email.split('@')
            if len(parts) == 2 and parts[1]:
                self.email_domain = parts[1]
            else:
                self.email_domain = False
        else:
            self.email_domain = False
       

            


    



            

  

