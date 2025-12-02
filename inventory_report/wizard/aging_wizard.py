from odoo import models, fields, api
from odoo.exceptions import UserError

class InventoryAgingWizard(models.TransientModel):
    _name = 'inventory.aging.wizard'
    _description = 'Inventory Age Report'

    report_based_on = fields.Selection([
        ('warehouse', 'Warehouse'),
        ('location', 'Location')
    ], string="Report Based On", required=True, default='warehouse')

    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    location_ids = fields.Many2many('stock.location', string='Locations',domain="[('usage','=','internal')]")
    include_all_products = fields.Boolean(string='Include All Products', default=True)
    product_id = fields.Many2one('product.product', string='Product',domain=[])

    
    def _get_product_domain(self):
        return []

    
    @api.onchange('include_all_products', 'warehouse_ids', 'location_ids', 'report_based_on')
    def _onchange_products_domain(self):

        # If "Include All Products" is checked
        if self.include_all_products:
            self.product_id = False
            return {'domain': {'product_id': []}}

        Product = self.env['product.product']

        # Determine locations based on selection
        if self.report_based_on == 'warehouse' and self.warehouse_ids:
            locations = self.warehouse_ids.mapped('lot_stock_id').ids

        elif self.report_based_on == 'location' and self.location_ids:
            locations = self.location_ids.ids

        else:
            locations = []

        # If locations selected → fetch products stored in those locations
        if locations:
            products = Product.search([
                ('qty_available', '>', 0),
                ('stock_quant_ids.location_id', 'in', locations)
            ])
        else:
            products = Product.search([])

        # Reset product if product not in domain
        if self.product_id and self.product_id.id not in products.ids:
            self.product_id = False

        return {'domain': {'product_id': [('id', 'in', products.ids)]}}



    def action_generate_report(self):
        Report = self.env['inventory.aging.wizard']
        Report.search([]).unlink()
        Report.create({

            "warehouse_name": "Warehouse A",
            "product_id": 1,
            "total_qty": 10,
        })

        return self.env.ref('inventory_report.inventory_age_xlsx_report').report_action(Report)











  