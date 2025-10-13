from odoo import models, fields, api
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError

class JobOpening(models.Model):
    _name = 'job.opening'
    _description = 'Job Opening'

    name = fields.Char(string="Name")
    job_id = fields.Many2one('job.position', string="Job Position")

