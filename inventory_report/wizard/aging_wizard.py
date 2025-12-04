# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64
import io
from openpyxl import Workbook
from openpyxl.styles import Font


class InventoryAgingWizard(models.TransientModel):
    _name = 'inventory.aging.wizard'
    _description = 'Inventory Aging Report Wizard'

    report_based_on = fields.Selection([
        ('warehouse', 'Warehouse'),
        ('location', 'Location')
    ], default='warehouse', required=True)

    warehouse_ids = fields.Many2many('stock.warehouse')
    location_ids = fields.Many2many(
        'stock.location',
        domain="[('usage', '=', 'internal')]"
    )

    include_all_products = fields.Boolean(default=False)
    line_ids = fields.Many2many (
        'inventory.aging.wizard.line',
       
        string="Inventory Aging Lines"
    )

    file_name = fields.Char(default="Inventory_Aging_Report.xlsx")
    file_data = fields.Binary()

    @api.onchange('report_based_on', 'warehouse_ids', 'location_ids', 'include_all_products')
    def _onchange_load_products(self):
        self.line_ids.unlink()

        if self.report_based_on == 'warehouse' and self.warehouse_ids:
            # For warehouses → use lot_stock_id for each selected warehouse
            locs = self.warehouse_ids.mapped('lot_stock_id')
        else:
            locs = self.location_ids

        # Fetch all child locations
        if locs:
            locs = self.env['stock.location'].search([('id', 'child_of', locs.ids)])

        location_ids = locs.ids if locs else []
        ctx = {'location': location_ids} if location_ids else {}

      
        if self.include_all_products:
            products = self.env['product.product'].search([('type', '=', 'product')])
        else:
            if location_ids:

                quants = self.env['stock.quant'].search([
                    ('location_id', 'child_of', location_ids),
                    ('quantity', '>', 0)
                ])
                products = quants.mapped('product_id')
            else:
                products = self.env['product.product']

        total_qty_all = 0
        total_value_all = 0

        for p in products:
            qty = p.with_context(ctx).qty_available
            virtual = p.with_context(ctx).virtual_available

            total_qty_all += qty + virtual
            total_value_all += qty * p.standard_price

        total_qty_all = total_qty_all or 1.0
        total_value_all = total_value_all or 1.0

        # -----------------------------
        # 4. Create Wizard Lines
        # -----------------------------
        lines = []
        for p in products:
            qty = p.with_context(ctx).qty_available
            virtual = p.with_context(ctx).virtual_available
            value = qty * p.standard_price

            quants_all = self.env['stock.quant'].search([
            ('product_id', '=', p.id),
            ('location_id.usage', '=', 'internal')
            ])
            overall_qty = sum(quants_all.mapped('quantity'))

            lines.append((0, 0, {
                'product_id': p.id,
                'default_code': p.default_code,
                'name': p.name,
                'list_price': p.list_price,

                'qty_available': qty,
                'virtual_available': virtual,

                'total_qty': qty + virtual,
                'overall_qty': overall_qty,
                'oldest_qty': qty,

                'value_dollar': value,
                'percent_value': (value / total_value_all) * 100,
                'average_cost': p.standard_price,
                'average_sale_price': p.list_price,
                'current_cost': p.standard_price,
                'current_sale_price': p.list_price,
            }))
            print("line////////////////", lines)

        self.line_ids = lines

 
    def action_generate_report(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Inventory Aging Report"

        headers = [
            "ID", "Reference", "Product Name", "Sale Price",
            "Qty On Hand", "Virtual Available", "Total Qty",
            "Overroll Oty", "Value ($)", "Percent Value",
            "Avg Cost", "Avg Sale Price", "Current Sale Price", "Current Cost"
        ]
        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for line in self.line_ids:
            print("line data///////", line.total_qty)
            ws.append([
                line.product_id.id,
                line.default_code,
                line.name,
                round(line.list_price, 2),
                round(line.qty_available, 2),
                round(line.virtual_available, 2),
                round(line.total_qty, 2),
                round(line.overall_qty, 2),
                round(line.oldest_qty, 2),
                round(line.value_dollar, 2),
                round(line.percent_value, 2),
                round(line.average_cost, 2),
                round(line.average_sale_price, 2),
                round(line.current_sale_price, 2),
                round(line.current_cost, 2),
            ])

        fp = io.BytesIO()
        wb.save(fp)
        fp.seek(0)
        self.write({
            'file_data': base64.b64encode(fp.read()),
            'file_name': f"Inventory_Aging_Report_{fields.Date.today()}.xlsx"
        })
        fp.close()

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/?model=inventory.aging.wizard&id={self.id}&field=file_data&filename_field=file_name&download=true',
            'target': 'self',
        }


class InventoryAgingWizardLine(models.TransientModel):
    _name = 'inventory.aging.wizard.line'
    _description = 'Inventory Aging Report Line'
    _order = 'qty_available DESC'

    
    product_id = fields.Many2one('product.product')

    default_code = fields.Char()
    name = fields.Char()
    barcode = fields.Char()
    list_price = fields.Float()

    qty_available = fields.Float()
    virtual_available = fields.Float()

    total_qty = fields.Float()
    overall_qty = fields.Float(string="Overall Qty")

    oldest_qty = fields.Float()

    value_dollar = fields.Float()
    percent_value = fields.Float()

    average_cost = fields.Float()
    average_sale_price = fields.Float()

    current_cost = fields.Float()
    current_sale_price = fields.Float()
