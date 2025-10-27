{
    'name': 'StudentManagement',
    'version': '1.0',
    'summary': 'Manage student records',
    'sequence': -101,
    'description': 'A simple module to manage students',
    'category': 'Education',
    'author': 'Wanbuffer Service',
    'depends': ['base','mail','website','portal'],
    'data': [
            'security/student_security.xml',
            'security/ir.model.access.csv',
            'security/student_rules.xml',
        
            'data/ir_sequence_data.xml',

            'views/student_views.xml',
            'views/student_register.xml',
            'views/subject_view.xml',
            'views/menuitem_view.xml',
            'views/student_portal_template.xml',
            'views/student_profile_view.xml',
            'views/tearchar_view.xml',
            'views/student_addmission_temp.xml',
           
            # 'views/menuitem_view.xml',

           
            'views/cron_unpaidfees_reminder.xml',
            

            'data/cron_archive_student.xml',
            'wizard/wizard_views.xml',
            
            'report/student_report_template.xml',
            'report/student_report.xml',

            ],
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png',],
    'license': 'LGPL-3',      
}





