from odoo import models,fields


class SendStudentEmail(models.TransientModel):
    _name="send.student.email"
    _descriptions="Student send email"


    email_from=fields.Char(string="Email From")
    email_to=fields.Char(string="Email To")
    email_sub=fields.Text(string="Email Subject")
    email_body=fields.Text(string="Email Body")