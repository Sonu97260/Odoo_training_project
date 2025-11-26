
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from psycopg2 import errors
import base64

class JobPortalController(http.Controller):
    
    @http.route(['/jobs'], type="http", auth="public", website=True)
    def jobs_list(self, **kwargs):
        jobs = request.env['job.position'].sudo().search([('active', '=', True)])
        return request.render('job_portal.job_page_template_id', {'jobs': jobs})

    @http.route(['/jobs/apply/<int:job_id>'], type="http", auth="public", website=True)
    def job_apply(self, job_id, **post):
        job = request.env['job.position'].sudo().browse(job_id)
        return request.render('job_portal.job_apply_template_id', {'job': job})

    @http.route(['/jobs/submit'], type="http", auth="public", methods=["POST"], website=True, csrf=False)
    def job_submit(self, **post):
        file = post.get("cv_attachment")
        cv_attachment = False

        job_id = post.get("job_id")
        if not job_id:
            return request.not_found()
        try:
            job_id = int(job_id)
        except Exception:
            return request.not_found()
        
        if file and hasattr(file, 'filename') and hasattr(file, 'read'):
                cv_attachment = base64.b64encode(file.read())
        vals = {
                "name": post.get("name"),
                "email": post.get("email"),
                "phone": post.get("phone"),
                "cv_attachment": cv_attachment,
                'job_id': job_id,
            }
        application = request.env['job.application'].sudo().create(vals)
        return request.redirect('/jobs/success/%d' % application.id)
        

    @http.route(['/jobs/success/<int:app_id>'], type="http", auth="public", website=True)
    def job_success(self, app_id, **kwargs):
        application = request.env['job.application'].sudo().browse(app_id)
        if not application:
            return request.not_found()
        return request.render('job_portal.job_success_page', {
            'application': application,
            'job': application.job_id,
        })