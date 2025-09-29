from odoo import models, fields,api
from odoo.http import request 
from odoo.exceptions import ValidationError 
from datetime import date,timedelta


class Teachar(models.Model):
    _name="teacher.teacher"
    _description = "Teacher"

    name=fields.Char(string="Teachar Name",required=True)
    contact_num=fields.Char(string="Teachar Contact number")
    email=fields.Char("Email",size=30)
    gender=fields.Selection([('male','Male'),('female','Female')], default='male')
    address=fields.Char(string="address")

    student_id=fields.One2many('rest.student','teacher_id',string='Student')

    date_request=fields.Date(string="Date")
    # category_id=fields.Many2one('hr.department',string='Category')	
    count_student=fields.Integer(string="Count Student", compute="_count_student")
    # user_id=fields.Many2one('res.users',string="user")


    @api.depends('count_student')
    def _count_student(self):
        for rec in self:
            rec.count_student=len(rec.student_id)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Example: validate unique teacher_id
            if self.env['rest.teachar'].search([('teacher_id', '=', vals.get('teacher_id'))], limit=1):
                raise ValidationError('A teacher with this ID already exists.')

            # Example: assign sequence if needed
            vals['sequence'] = self.env["ir.sequence"].next_by_code('teacher.custom.sequence')

        return super().create(vals_list)   




