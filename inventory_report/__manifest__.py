{
    'name': 'inventory_report',
    'category': 'Inventory',
    'summary': 'Inventory Reporting Enhancements',
    'version': '1.0',
    'sequence': -101,
    'depends': ['base','stock','web','product'],
    'data': [
        'secruity/ir.model.access.csv',
        'wizard/aging_wizard_views.xml',
        # 'views/aging_report_views.xml',
    
    ],
    'installable': True,
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}