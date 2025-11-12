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

        'views/res_settings_view.xml',
        'views/crm_lead_view.xml',

        # 'views/wizard_view.xml',
        
        ],
    'assets': {
    'web.assets_backend': [
        'static/src/js/crm.js',
        
    ],
},
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    }