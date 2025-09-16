{
    'name': 'JobPortal',
    'version': '1.0',
    'summary': 'Manage jobs application and position',
    'sequence': -100,
    'description': 'A simple module to manage jobs',
    'category': 'category',
    'author': 'Wanbuffer Service',
    'depends': ['base','hr','website','portal','mail'],
    'data': [
            'security/ir.model.access.csv',
            'security/hr_secrutiy.xml',
            'security/public_job_rule.xml',

            'data/cron_active_job.xml',
            'data/job_server_action.xml',
           
   
            'views/job_application_view.xml',
            'views/job_position_view.xml',
            'views/menu_item_view.xml',
            'views/job_template.xml',
            'views/email_template.xml',
            
            ],
    'installable': True,
    'application': True,
    # 'images': ['static/description'],
    'license': 'LGPL-3',      
}






