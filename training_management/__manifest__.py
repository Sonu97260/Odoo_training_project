{
    "name": "training_management",
    "version": "1.0",
    "summary": "Manage teacher and student information",
    "sequence":-101,
    "category": "Education",
    "author": "Wan Buffer",
    'depends': ['base', 'web'],
   	'data': [
                # 'security/student_security.xml',
                'views/menu_item.xml',
                'security/student_rule.xml',
				'security/ir.model.access.csv',
            
                'views/student_view.xml',
                'views/teacher_view.xml',
            
			
			],
    'assets': {
        'web.assets_backend': [
            'StudentManagement/static/src/js/dashboard.js',
            'StudentManagement/static/src/xml/dashboard.xml',
        ],
    },
    "installable": True,
    "application": True,
    'images': ['static/description/icon.png',],
    # "icon": "static/descrition/icon.png",
    "license": "LGPL-3",
}






