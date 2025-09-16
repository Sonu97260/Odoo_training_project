# applicant_name, email, phone, cv_attachment (binary),
# job_id (Many2one to job.position)
# status (selection: draft, submitted, shortlisted, rejected, hired)

from odoo import models, fields,api# type: ignore
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError # type: ignore
from datetime import date,timedelta
import logging


class JobApplication(models.Model):
    _name="job.application"
    _description="Job application"

    name=fields.Char(string="Name")
    email=fields.Char(string="Email")
    phone=fields.Char(string="Phone")
    cv_attachment=fields.Binary(string="CV attachment",attachment=True,help="upload the cv here")
    job_id=fields.Many2one('job.position',string="Jobs")
    status=fields.Selection([
        ('draft','draft'),
        ('submitted','submitted'),
        ('shortlisted','shortlisted'),
        ('rejected','rejected'),
        ('hired','hired')])
    
    email_domain=fields.Char(string="Email Domain")

    @api.onchange('email')
    def _onchange_email(self):
        if self.email and "@" in self.email:
            self.email_domain = self.email.split('@')[-1]
        else:
            self.email_domain = False


    def action_draft(self):
        self.write({'status': 'draft'})

    def action_submitted(self):
        self.write({'status': 'submitted'})

    def action_shortlisted(self):
        self.write({'status': 'shortlisted'})

    def action_rejected(self):
        self.write({'status': 'rejected'}) 

    def action_hire(self):
        self.write({'status': 'hired'})             


    def send_email(self):
        job=self.search([('status','=','shortlisted')])
        for rec in job:
            if rec.email:
                template=self.env.ref('JobPortal.job_shortlisted_email_template')
                template.send_mail(rec.id)
               



            

  

