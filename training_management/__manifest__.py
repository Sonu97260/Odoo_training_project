{
    "name": "training_management",
    "version": "1.0",
    "summary": "Manage teacher and student information",
    "sequence":-101,
    "category": "Education",
    "author": "Wan Buffer",
    'depends': ['base'],
   	'data': [
                # 'security/student_security.xml',
                'security/student_rule.xml',
				'security/ir.model.access.csv',
            
        
                'views/student_view.xml',
                'views/teacher_view.xml',
                'views/menu_item.xml',
			
			],
    "installable": True,
    "application": True,
    'images': ['static/description/icon.png',],
    # "icon": "static/descrition/icon.png",
    "license": "LGPL-3",
}






