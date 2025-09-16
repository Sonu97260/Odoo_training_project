from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import base64

class JobPortal(http.Controller):

    @http.route(['/jobs'], type="http", auth="public", website=True)
    def jobs_list(self, **kwargs):
        jobs = request.env['job.position'].sudo().search([('active', '=', True)])
        return request.render('JobPortal.job_page_template_id', {'jobs': jobs})
    
    @http.route(['/jobs/apply/<int:job_id>'], type="http", auth="public", website=True, csrf=True)
    def job_apply(self, job_id, **post):
        job = request.env['job.position'].sudo().browse(job_id)
        print("job apply...........................",job)
        # if not job or not job.active:    
        #     return request.not_found()

        if request.httprequest.method == 'POST':
          
            name = post.get('name')
            email = post.get('email')
            phone = post.get('phone')
            cv_file = request.httprequest.files.get('cv_attachment')

            if not name or not email:
                raise ValidationError("Name and Email are required.")

            job = request.env['job.application'].sudo().create({
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'cv_attachment': cv_file.read() if cv_file else False,
                    'job_id': job_id})

            return request.render('JobPortal.job_success_page', {'job': job})
        return request.render('JobPortal.job_apply_template_id', {'job': job})
