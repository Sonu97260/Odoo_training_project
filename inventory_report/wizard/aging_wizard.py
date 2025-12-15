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
    line_ids = fields.One2many(
    'inventory.aging.wizard.line',
    'wizard_id',
    string="Inventory Aging Lines"
    )


    file_name = fields.Char(default="Inventory_Aging_Report.xlsx")
    file_data = fields.Binary()

    @api.onchange('report_based_on', 'warehouse_ids', 'location_ids', 'include_all_products')
    def _onchange_load_products(self):
        self.ensure_one()
        self.line_ids = [(5, 0, 0)]

        if self.report_based_on == 'warehouse':
            if not self.warehouse_ids:
                return
            base_locs = self.warehouse_ids.mapped('lot_stock_id')
        else:
            if not self.location_ids:
                return
            base_locs = self.location_ids

        # include child locations
        all_locs = self.env['stock.location'].search([
            ('id', 'child_of', base_locs.ids),
            ('usage', '=', 'internal')
        ])

        location_ids = all_locs.ids
        ctx = {'location': location_ids}


        if self.include_all_products:
            quants = self.env['stock.quant'].search([
                ('location_id', 'in', location_ids)
            ])
            products = quants.mapped('product_id')
        else:
            quants = self.env['stock.quant'].search([
                ('location_id', 'in', location_ids),
                ('quantity', '>', 0)
            ])
            products = quants.mapped('product_id')


        if not products:
            return

        qty_map = {}
        quants_all = self.env['stock.quant'].search([
            ('location_id', 'in', location_ids)
        ])

        for q in quants_all:
            qty_map[q.product_id.id] = qty_map.get(q.product_id.id, 0) + q.quantity


        total_value_all = sum(
            qty_map.get(p.id, 0) * (p.standard_price or 0)
            for p in products
        ) or 1.0

        lines = []
        for p in products:
            qty = qty_map.get(p.id, 0.0)
            virtual = p.with_context(ctx).virtual_available or 0.0

            value = qty * (p.standard_price or 0)
            percent = (value / total_value_all) * 100

            lines.append((0, 0, {
                # 'product_id': p.id,
                'default_code': p.default_code,
                'name': p.name,
                'barcode': p.barcode,

                'qty_available': qty,
                'virtual_available': virtual,
                'total_qty': qty + virtual,
                'overall_qty': qty,
                'oldest_qty': qty,

                'value_dollar': value,
                'percent_value': percent,

                'average_cost': p.standard_price,
                'average_sale_price': p.list_price,
                'current_cost': p.standard_price,
                'current_sale_price': p.list_price,
            }))

        self.line_ids = lines


    def action_generate_report(self):
        wb = Workbook()
        ws = wb.active
        ws.title = "Inventory Aging Report"

        headers = [
            "ID", "Reference", "Product Name", 
            "Total Qty",
            "Overroll Oty", "Value", "Percent Value",'Oldest qty',
            "Avg Cost", "Avg Sale Price", "Current Sale Price", "Current Cost"
        ]
        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for line in self.line_ids:
            ws.append([

                line.product_id.id,
                line.default_code,
                line.name,
                round(line.total_qty, 2),
                round(line.overall_qty, 2),
                round(line.value_dollar, 2),
                round(line.percent_value, 2),
                round(line.oldest_qty, 2),
                round(line.average_cost, 2),
                round(line.average_sale_price, 2),
                round(line.current_cost, 2),
                round(line.current_sale_price, 2),
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

    wizard_id = fields.Many2one('inventory.aging.wizard', ondelete='cascade')

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
