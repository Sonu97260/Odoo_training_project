from odoo import models, fields,api# type: ignore
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError # type: ignore
from datetime import date,timedelta
import logging
import re

_logger = logging.getLogger(__name__)


class StudentClass(models.Model):
    _name='student.class'
    _description=' Student Classes'

    name=fields.Char(string='Name')

class StudentSubject(models.Model):
    _name='student.subject'
    _description='Student Subject'

    subject=fields.Char(string='Subject')
    code=fields.Char(string='Subject code')    

class Student(models.Model):
    _name = 'rest.student'
    _description = 'Student'
    _inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]

    sequence=fields.Char(string="sequence")
    name = fields.Char(string='Name', required=True)
    student_id=fields.Char(string='Roll no',unique=True)
    dob=fields.Date(string='Date of birth')
    age=fields.Integer(string='Age',compute='_compute_age',store=True)
    is_minor=fields.Boolean('Is Minor')
    gender=fields.Selection([('female','Female'),('male','Male')],string="Gender")
    class_id=fields.Many2one('student.class',string="Classes")
    # subject_id=fields.Many2many('school.subject',string='Subjects')
    admission_date=fields.Date(string='Admission Date')
    image=fields.Image(string="Image", max_width=128, max_height=128)
    color = fields.Integer('Color Index', default=0)
    course=fields.Char(string="Course")
    state=fields.Selection([
    ('draft','draft'),
    ('confirmed','confirmed'),
    ('apporved','apporved'),
    ('cancelled','cancelled')]
    ,default='draft',string="State",tracking=True)

    username=fields.Char(string="username")
 
    guardian_name = fields.Char(string="Guardian Name")
    guardianphone = fields.Char(string="Guardian Phone No", size=15)

    teacher_id=fields.Many2one('teacher.teacher',string="teachar name")

    email=fields.Char(string="Email") 

    _sql_constraints = [
        ('unique_email', 'unique(email)', 'Email must be unique!'),
        ('unique_student_id', 'unique(student_id)', 'Student id must be unique!')
    ]      
    phone=fields.Char(string="Phone",size=64)

    active = fields.Boolean(default=True)

    maths=fields.Float(string="Maths")
    english=fields.Float(string="English")
    gujarati=fields.Float(string="Gujarati")
    total=fields.Float(string="Total",compute='_calculate_total',store=True)
    status=fields.Selection([('draft','Draft'),('feepaid','Feepaid'),('unpaid','Unpaid')],default='draft')
    unpaid_date=fields.Date(string="Unpaid date")
    subject_id=fields.Many2many('school.subject',string="Subjects")
    
    user_id=fields.Many2one('res.users',string="Realted user",ondelete="cascade")

   
    #def chech_orm(self):
    #    search_var=self.env['rest.student'].browse(12)
    #    print("search var///////////////////",search_var)


    def send_email(self):
        action_ref=self.env.ref('StudentManagement.action_send_student').read()[0]
        action_ref['context']={
            'default_email_from':'test@123gmail.com',

        }
        return action_ref
    
    # def show_rainbow(self):
    #     return{
    #         'effect':
    #         {
    #             'fadeout':'slow',
    #             'message':'this is the rainbow effect .Congrats you have done it.',
    #             'img_url':'/web/static/img/smile.svg',
    #             'type':'rainbow_man',
    #         }
    #     }
    def get_active_student_count(self):
        count = self.search_count([('active', '=', True)])
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Active Students',
                'message': f'Total Active Students: {count}',
                'type': 'success',
             }                                  
        }
    def unpaidfees_student_reminder(self):
        students=self.search([('status','=','unpaid')])
        for student in students:
            if student.email:
                template=self.env.ref('StudentManagement.email_unpaid_student_id')
                template.send_mail(student.id)
                print("unpaid fees reminder...............................")
            
    
    def report_student(self):
        report=self.env.ref('StudentManagement.student_report_id').read()[0]
        return report

    # @api.constrains('age')
    # def val_age(self):
    #     for record in self:
    #         if record.age <=18:
    #             raise ValidationError("the age must be 18 above.")
            
    @api.constrains('email')       
    def val_email(self):
        if self.email:
           match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)

        if match==None:
            raise ValidationError("please enter the valid email id")          

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env['rest.student'].search([('student_id', '=', vals.get('student_id'))], limit=1):
                raise ValidationError('A student with this student id already exists.')
            vals['sequence'] = self.env["ir.sequence"].next_by_code('student.custom.sequence')


        if vals.get('email') and vals.get('password'):
            user = self.env['res.users'].create({
                'name': vals.get('name'),
                'login': vals.get('email'),
                'email': vals.get('email'),
                'password': vals.get('password'),
                'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
            })
            vals['user_id'] = user.id

        return super().create(vals_list)
    
    def write(self,vals):
        existing_students=self.env['rest.student'].search([])
        if 'status' in vals:
            # Example: log a message
            self.env['mail.message'].create({
                'subject': f"Status changed to {vals['status']}",
                'body': f"Student(s) {', '.join(self.mapped('name'))} updated",
                'model': 'rest.student',
                'res_id': self.id,
            })
        for student in existing_students:
            if student.student_id == vals.get('student_id'):
                raise ValidationError('A student with this student id is exists.')
        return super().write(vals)

    # def unpaid_student(self):
    #     for rec in self:
    #         self.status='unpaid'
	# 		# self.write({'status':'unpaid'})
		   
    # def feepaid_student(self):
	#     for rec in self:
    #             self.status='feepaid'
	# 		# self.write({'status':'feespaid'})
			
    def auto_archive_students(self):
        print("Cron running...")

        one_year_ago = date.today() - timedelta(days=365)
        students_to_archive = self.search([
        ('admission_date','<', one_year_ago),
        ('active', '=', True),
        ])

        print(" Found students:", students_to_archive)
        students_to_archive.write({'active': False})

    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                rec.age= date.today().year - rec.dob.year
            else:
                rec.age = 0  

    @api.depends('maths','english','gujarati')
    def _calculate_total(self):
        for rec in self:
            rec.total= (rec.maths)+(rec.english)+(rec.gujarati)
            _logger.info("Computed total for %s: %s", rec.name, rec.total)
            print("compute total...................")
        
    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 18:
            self.is_minor = True
        else:
            self.is_minor = False



    def action_confirm(self):
        for rec in self:
            rec.state="confirmed"

    def action_approve(self):
        for rec in self:
            rec.state="apporved"


    def action_cancel(self):
        for rec in self:
            rec.state="cancelled"

    def send_addmission_email(self):
        template=self.env.ref('StudentManagement.email_student_addmission_id')
        for student in self:
            if student.email:
                template.send_mail(student.id)
                print("admission email sent...............................")



            



