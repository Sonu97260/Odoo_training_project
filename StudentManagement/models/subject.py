from odoo import models,fields,api


class Subject(models.Model):
	_name="school.subject"
	_description="School Subject"

	name=fields.Char(string="Subject Name",required=True)