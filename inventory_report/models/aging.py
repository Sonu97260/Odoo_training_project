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


    def get_report_lines(self):
        self.ensure_one()
        lines = []

        # Determine locations exactly like in your domain logic
        location_ids = self.env['stock.location']
        if self.report_based_on == 'warehouse' and self.warehouse_ids:
            for wh in self.warehouse_ids:
                location_ids |= wh.lot_stock_id | wh.lot_stock_id.child_ids
        elif self.report_based_on == 'location' and self.location_ids:
            for loc in self.location_ids:
                location_ids |= loc | loc.child_ids

        domain = [('location_id', 'in', location_ids.ids), ('quantity', '>', 0)]
        if not self.include_all_products:
            domain += [('product_id', 'in', self.product_ids.ids)]

        quants = self.env['stock.quant'].search_read(domain, [
            'product_id', 'quantity', 'location_id', 'lot_id'
        ])

        product_ids = [q['product_id'][0] for q in quants]
        products = self.env['product.product'].browse(product_ids).with_context(
            location=location_ids.ids
        )

        for product in products:
            lines.append({
                'default_code': product.default_code or '',
                'name': product.name,
                'list_price': product.list_price,
                'quantity': product.qty_available,
                'virtual_quantity': product.virtual_available,
                'barcode': product.barcode or '',
                'currency_id': self.env.company.currency_id,
            })

        return lines
        
