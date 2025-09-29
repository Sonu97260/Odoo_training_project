from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class Mycontroller(http.Controller):

    @http.route('/student/register', type="http", auth="public", website="True", csrf=False)
    def student_register_form(self, **kwargs):
        student = request.env['rest.student'].sudo().search([])
        return request.render("StudentManagement.student_register_template_id", {'student':student})

    @http.route('/student/register/submit', type='http', auth='public', csrf=False, website="True", methods=['POST'])
    def student_register_submit(self, **post):
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        gender = post.get('gender')
        course = post.get('courses')  # Changed from 'course' to match your template
        username = post.get('username')
        password = post.get('password')

      
        student = request.env['rest.student'].sudo().search([])

        if not all([name, email, username, password]):
            return request.render("StudentManagement.student_register_template_id", {
                'error_message': 'Please fill in all required fields.',
                'form_data': post  # To preserve form data
            })

        # User = request.env['res.users'].sudo()
        
        # Check if username (login) already exists
        existing_user_by_username = request.env['res.users'].sudo().search([('login','=',username)],limit=1)
        if existing_user_by_username:
            return request.render("StudentManagement.student_register_template_id", {
                'error_message': 'This username is already registered. Please login instead',
                'form_data': post
            })
        
        # Check if email already exists
        # existing_user_by_email = User.search([('email', '=', email)], limit=1)
        # if existing_user_by_email:
        #     return request.render("StudentManagement.student_register_template_id", {
        #         'error_message': 'Email already exists! Please use a different email.',
        #         'form_data': post
        #     })

        try:
            # Create a new user
            portal_group=request.env.ref('base.group_portal')
            user=request.env['res.users'].sudo().create({
                'name': name,
                'login': username,  # Use username as login
                'email': email,
                'password': password,
                'groups_id': [(6, 0, [portal_group.id])],  # Portal user group
            })

            # Create student Profile  record
            student = request.env['rest.student'].sudo().create({
                'name': name,
                'email': email,
                'phone': phone,
                'gender': gender,
                'course': course,
                'username': username,
                'password': password,
                'user_id': user.id,
            })

            return request.render("StudentManagement.student_register_success_id", {
                'student_name': name
            })

        except Exception as e:
            _logger.error("Student registration failed: %s", str(e))
            return request.render("StudentManagement.student_register_template_id", {
                'error_message': 'Registration failed: %s' % str(e),
                'form_data': post
            })

     #student Profile page   
    @http.route('/student/profile',type='http', auth='user', csrf=False, website="True", methods=['POST'])
    def student_profile(self,  **kwargs):
        student = request.env['rest.student'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        return request.render("StudentManagement.student_profile_portal", {'student': student})

        # if not student:
        #     return request.render("StudentManagement.student_profile_portal")
        
     #Student Login page
    @http.route('/student/login', type='http', auth='public', website=True)
    def student_login_form(self, **kw):
        message = kw.get('message')
        context = {}
        
        if message == 'please_login':
            context['info'] = 'Registration successful! Please login with your credentials.'
            
        return request.render('StudentManagement.student_login_template', context)
    
    @http.route('/student/login/submit',type='http', auth='public', csrf=False, website="True", methods=['POST'])
    def student_login_submit(self,  **post): 
        username= post.get('username')  
        password = post.get('password')

        if not username or not password:
            return request.render('StudentManagement.student_login_template',{
                'error':'email and password is required',
            })
        
        student = request.env['rest.student'].sudo().search([
            ('username', '=', username),
            ('password', '=', password),
            ], limit=1)

        if student:
            return request.redirect('/student/profile')


        return request.render('StudentManagement.student_login_template', {
            'error': 'Invalid Email ID or Password'
        })

        


            

















    
