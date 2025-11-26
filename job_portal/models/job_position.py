
from odoo import models, fields,api# type: ignore
from odoo.http import request # pyright: ignore[reportMissingImports]
from odoo.exceptions import ValidationError # type: ignore
from datetime import date,timedelta
import logging

class JobPosition(models.Model):
	_name="job.position"
	_description="Job Position"
	# _inherit = ['mail.thread']
	_inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]
	

	name=fields.Char(string='name')
	description=fields.Char(string="Description")
	department_id=fields.Many2one('hr.department',string="Department",tracking=True)
	active = fields.Boolean(default=True)
	application_count=fields.Integer(string='Applications',compute='_count_application',store=True)
	
	total_openings = fields.One2many('job.opening', 'job_id', string="Total Openings")
	# Computed total
	total = fields.Integer(string="Total Openings", compute='_cal_total_opening', store=True)



	def active_jobs(self):
		count = self.search_count([('active', '=', True)])
		return {
			'type': 'ir.actions.client',
			'tag': 'display_notification',
			'params': {
				'title': 'Active Jobs',
				'message': f'Total Active Jobs: {count}',
				'type': 'success',
			}                                  
		} 

	@api.depends('total_openings')
	def _cal_total_opening(self):
		for rec in self:
			rec.total=len(rec.total_openings or [])

	@api.depends('application_count')
	def _count_application(self):
		for rec in self:
			if rec.id:
				rec.application_count = self.env['job.application'].search_count([('job_id', '=', rec.id)])
			else:
				rec.application_count = 0


	@api.model
	def get_dashboard_data(self):
		total = self.search_count([])
		return {
			'total': total,
		}


	

