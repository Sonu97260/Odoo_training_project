{
    "name": "job_portal",
    "version": "1.0",
    "summary": "Manage jobs application and position",
    "sequence":-100,
    "category": "Human Resources",
    "author": "Wan Buffer",
    'depends': ['base','hr','website','portal'],
   	'data': [
				'data/cron_active_job.xml',
				# 'views/email_template.xml',
				# 'data/job_server_action.xml',
                'views/job_approve_template.xml',
                'data/job_approve_app.xml',
                
				'security/hr_security.xml',
				'security/ir.model.access.csv',
				# 'security/public_job_rule.xml',
			
				'views/job_position_view.xml',
                'views/job_application_view.xml',
                'views/job_template.xml',
                'views/menu_item_view.xml',
			
			],
    "installable": True,
    "application": True,
    "icon": "static/descrition/icon.png",
    "license": "LGPL-3",
}

# python3.10 odoo-bin --addons-path=addons,/home/rajan/workspace/enterprise/18.0,/home/rajan/workspace/custom_project -p 8888 -d jobportal_db  -i job_portal




