{
    'name': 'sale_customer',
    'version': '1.0',
    'category': 'Sales/Sales',
    'sequence': 5,
    'summary': 'From quotations to invoices',
    'website': 'https://www.odoo.com/app/sales',
    'depends': ['sale', 'digest','account'],
    'data': [
        'data/sale_action.xml',
        'views/action_mail_template.xml',
      
        'views/sale_order_view.xml',
        'views/invoice_order_view.xml',
        'views/report_invoice.xml',
        ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
      }