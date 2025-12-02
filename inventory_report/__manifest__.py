{
    'name': 'inventory_report',
    'category': 'Inventory',
    'summary': 'Inventory Reporting Enhancements',
    'version': '1.0',
    'sequence': -99,
    'depends': ['base', 'stock','web'],
    'data': [
        'secruity/ir.model.access.csv',
        'wizard/aging_wizard_views.xml',
        # 'report/report_template_excel.xml',
    ],
    'installable': True,
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}