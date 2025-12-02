from odoo import models, fields
from datetime import datetime

class InventoryAgingXlsx(models.AbstractModel):
    _name = 'inventory.aging.report'
    _description='inventory Aging Report XLSX'

    