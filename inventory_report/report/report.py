from odoo import models, fields
from datetime import datetime

class InventoryAgingXlsx(models.AbstractModel):
    _name = 'inventory.aging.report.line'
    _description='inventory Aging Report XLSX'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet("Aging Report")
        bold = workbook.add_format({'bold': True})

        headers = [
            'Warehouse', 'Product', 'Qty', 'Avg Cost',
            'Avg Sale Price', 'Current Cost'
            
        ]

        row = 0
        col = 0

        for h in headers:
            sheet.write(row, col, h, bold)
            col += 1

        row = 1

        for rec in partners:
            sheet.write(row, 0, rec.warehouse_id.name or "")
            sheet.write(row, 1, rec.product_id.name)
            sheet.write(row, 2, rec.qty)
            sheet.write(row, 3, rec.avg_cost)
            sheet.write(row, 4, rec.avg_sale)
            sheet.write(row, 5, rec.current_cost)
            row += 1
