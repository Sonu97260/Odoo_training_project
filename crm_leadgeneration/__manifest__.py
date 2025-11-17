{
    'name': 'crm_leadgeneration',
    'version': '1.0',
    'category': 'Crm',
    'sequence': 5,
    'summary': 'Crm lead generation',
    'website': 'https://www.odoo.com/app/sales',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'wizard/wizard_view.xml',
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    }