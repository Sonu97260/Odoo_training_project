from odoo import models, fields,api# type: ignore
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError # type: ignore
from datetime import date,timedelta
import logging
_logger = logging.getLogger(__name__)


# Task 1 – Model Enhancements 
# Add a new model training.teacher with fields: name, email, expertise.
# Link it with students (Many2many).
# Compute a new field student_count on teacher model.

class Teacher(models.Model):
    _name='training.teacher'
    _description='Teacher Information'

    name=fields.Char(string='Name',required=True)
    email=fields.Char(string='Email',required=True)
    expertise=fields.Char(string='Expertise',required=True)
    student_ids=fields.Many2many('training.student',string='Students')
    student_count=fields.Integer(string='Student Count',compute='_compute_student_count')


    @api.depends('student_ids')
    def _compute_student_count(self):
        for teacher in self:
            teacher.student_count = len(teacher.student_ids)
            