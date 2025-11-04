from odoo import models,fields,api


class Subject(models.Model):
	_name="school.subject"
	_description="School Subject"

	name=fields.Char(string="Subject Name",required=True)


	@api.model
	def get_subject_count(self):
		subject_model = self.env['school.subject']
		print("total_subject/....../////////")
		total_subject = subject_model.search_count([])
		return {
        	'total_subject': total_subject,
    	}
		