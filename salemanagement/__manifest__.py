{
    'name': 'salemanagement',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 5,
    'summary': 'From quotations to invoices',
    'website': 'https://www.odoo.com/app/sales',
    'depends': ['mail','sale', 'digest','account'],
    'data': [
        'data/sale_order_cron.xml',
       'data/sale_server_action.xml',

        'report/sale_order_report.xml',
    
        'views/sale_email_template.xml',
        'views/sale_order_view.xml',
        'views/action_mail.xml',

        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    }