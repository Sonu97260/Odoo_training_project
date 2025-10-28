from odoo import models, fields,api# type: ignore
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError # type: ignore
from datetime import date,timedelta
import logging
_logger = logging.getLogger(__name__)

class Student(models.Model):
    _name='training.student'
    _description='Student Information'


    name=fields.Char(string='Name',required=True)
    age=fields.Integer(string='Age',required=True)
    course=fields.Char(string='Course',required=True)
    user_id = fields.Many2one('res.users', string="Assigned User", default=lambda self: self.env.user)

# Add a state field to training.student (draft, confirmed, alumni).
    state=fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('alumni','Alumni')
    ],string='state',default='draft',tracking=True)

    
    def action_set_draft(self):
        for record in self:
            record.state='draft'  

    def confirm_students(self):
        for record in self:
            record.state='confirmed'          

    def action_set_alumni(self):
        for record in self:
            record.state='alumni'                        

    @api.model
    def create(self, vals):
        if 'user_id' not in vals:
            vals['user_id'] = self.env.uid
        return super().create(vals)
    
    def write(self, vals):
        if 'user_id' not in vals:
            vals['user_id'] = self.env.uid
        return super().write(vals)



