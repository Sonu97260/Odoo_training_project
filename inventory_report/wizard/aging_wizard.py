from odoo import models, fields, api

class InventoryAgingWizard(models.TransientModel):
    _name = 'inventory.aging.wizard'
    _description = 'Inventory Aging Report Wizard'

    report_based_on = fields.Selection([
        ('warehouse', 'Warehouse'),
        ('location', 'Location')
    ], string="Report Based On", default='warehouse', required=True)

    warehouse_ids = fields.Many2many('stock.warehouse', string="Warehouse")
    location_ids = fields.Many2many('stock.location', string="Location", domain="[('usage', '=', 'internal')]")

    include_all_products = fields.Boolean(string="Include All Products", default=False)

  
    product_ids = fields.Many2many('product.product',string="Products",domain="[('type', '=', 'product')]")
    color = fields.Integer(default=8)
   
    product_domain = fields.Char(
        compute="_compute_product_domain",
        readonly=True,
        store=False,
    )

    from odoo import models, fields, api

class InventoryAgingWizard(models.TransientModel):
    _name = 'inventory.aging.wizard'
    _description = 'Inventory Aging Report Wizard'

    report_based_on = fields.Selection([
        ('warehouse', 'Warehouse'),
        ('location', 'Location')
    ], default='warehouse', required=True)

    warehouse_ids = fields.Many2many('stock.warehouse')
    location_ids = fields.Many2many('stock.location', domain="[('usage', '=', 'internal')]")

    include_all_products = fields.Boolean(default=False)

    product_ids = fields.Many2many(
        'product.product',
        domain="[('type', '=', 'product')]",
    )

    product_domain = fields.Char(compute="_compute_product_domain")

    @api.depends('warehouse_ids', 'location_ids', 'include_all_products', 'report_based_on')
    def _compute_product_domain(self):
        Quant = self.env['stock.quant']

        for wiz in self:
            # If "All products" → return default domain
            if wiz.include_all_products:
                wiz.product_domain = "[('type', '=', 'product')]"
                continue

            # Collect locations based on the selection
            location_ids = self.env['stock.location']

            if wiz.report_based_on == 'warehouse' and wiz.warehouse_ids:
                for wh in wiz.warehouse_ids:
                    location_ids |= wh.lot_stock_id | wh.lot_stock_id.child_ids

            elif wiz.report_based_on == 'location' and wiz.location_ids:
                for loc in wiz.location_ids:
                    location_ids |= loc | loc.child_ids

            if not location_ids:
                wiz.product_domain = "[('id', '=', False)]"
                continue

            # Fast Odoo 19-safe search → get quant IDs
            quant_ids = Quant._search([
                ('location_id', 'in', location_ids.ids),
                ('quantity', '>', 0),
            ])

            # Get product IDs from quants
            product_ids = Quant.browse(quant_ids).mapped('product_id.id')

            if product_ids:
                wiz.product_domain = f"[('id', 'in', {product_ids})]"
            else:
                wiz.product_domain = "[('id', '=', False)]"

    @api.onchange('warehouse_ids', 'location_ids', 'include_all_products', 'report_based_on')
    def _onchange_clear_products(self):
        if not self.include_all_products:
            self.product_ids = [(5, 0, 0)]


                
    @api.onchange('warehouse_ids', 'location_ids', 'include_all_products', 'report_based_on')
    def _onchange_clear_products(self):
        if not self.include_all_products:
            self.product_ids = [(5, 0, 0)]

    def action_generate_report(self):
        print("Generating Inventory Aging Report...")

    #     Report = self.env['inventory.aging.wizard']
    #     Report.search([]).unlink()
    #     Report.create({

    #         "warehouse_name": "Warehouse A",
    #         "product_id": 1,
    #         "total_qty": 10,
    #     })

    #     return self.env.ref('inventory_report.inventory_age_xlsx_report').report_action(Report)











  