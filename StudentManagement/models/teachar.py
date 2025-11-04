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
    sequence = fields.Char(string='Sequence', readonly=True)


    @api.depends('count_student')
    def _count_student(self):
        for rec in self:
            rec.count_student=len(rec.student_id)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            teacher_id = vals.get('teacher_id')
            if teacher_id:
                existing = self.env['teacher.teacher'].search([('teacher_id', '=', teacher_id)], limit=1)
                if existing:
                    raise ValidationError('A teacher with this ID already exists.')
            vals['sequence'] = self.env["ir.sequence"].next_by_code('teacher.custom.sequence')
        return super().create(vals_list)
    

    @api.model
    def get_teacher_count(self):
        teacher_model = self.env['teacher.teacher']
        total_teachers = teacher_model.search_count([])
        return {
            'total_teachers': total_teachers,
        }




