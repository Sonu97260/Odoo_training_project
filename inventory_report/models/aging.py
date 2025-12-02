from odoo import models, fields

class InventoryAgingReport(models.Model):
    _name = 'inventory.aging.report'
    _description = 'Inventory Aging Report'
    _order = 'product_id'

    warehouse_name = fields.Char("Warehouse")

    product_id = fields.Many2one('product.product', readonly=True)
    product_name = fields.Char(related="product_id.name", string="Product Name", store=True)
    product_reference = fields.Char(related="product_id.default_code", string="Reference", store=True)

    total_qty = fields.Float("Total Qty")
    qty_percent = fields.Float("Qty (% of Inventory)")
    oldest_qty = fields.Float("Oldest Qty")

    value = fields.Float("Value ($)")
    value_percent = fields.Float("Value (% of Inventory)")

    avg_cost = fields.Float("Average Cost")
    avg_sale_price = fields.Float("Average Sale Price")
    current_sale_price = fields.Float("Current Sale Price")
    current_cost = fields.Float("Current Cost")

    
