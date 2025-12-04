from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(
        string='Internal Reference',
        help="Internal reference for the product (e.g., SKU)."
    )
    name = fields.Char(
        string='Product Name',
        required=True,
        help="Display name of the product."
    )
    list_price = fields.Monetary(
        string='Sales Price',
        required=True,
        help="Standard selling price."
    )
    barcode = fields.Char(
        string='Barcode',
        help="International barcode (e.g., EAN13)."
    )

    # Stock fields are on product.product, but accessible via template
    