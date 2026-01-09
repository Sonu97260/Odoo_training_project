{
    'name': 'Advanced Task Timer',
    'version': '1.0',
    'category': 'Project',
    'summary': 'Task time tracking with timer',
    'depends': [
        'web',
        'project',
        'hr_timesheet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/kanban_view_task.xml',   

        'wizard/timer_wizard_view.xml',
        'wizard/end_timer_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'wb_advance_task_timer/static/src/xml/timer_button_popup.xml',
            'wb_advance_task_timer/static/src/js/timer_button_popup.js',
            'wb_advance_task_timer/static/src/js/kanban_view.js',
            # 'wb_advance_task_timer/static/css/buton.css',   
        
           
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
