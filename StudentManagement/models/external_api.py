# import requests
# import json
# from odoo import models,fields,api,_
# from odoo.exceptions import UserError


# class StudentApi(models.Model):
#     _inherit="rest.student"


#     external_id=fields.Char(string="External id",readonly=True)

#     def call_external_api(self):
#         for student in self:
#             url = "http://127.0.0.0:8069/"
#             headers={
#                 'Content-Type':'application/json',
#                 }
#             payload={
#                 'name':student.name,
#                 'email':student.email,
#                 'student_id':student.student_id,
#                 }
#         try:
#             response=requests.post(url,data=json.dumps(payload),headers=headers,timeout=30)
#             if response.status_code==200:
#                 result=response.json()
#                 student.external_id=result.get('id')
#                 return True
            
#             else:
#                 raise UserError(_("Api error  :%s")% response.text)
            
#         except requests.exceptions.RequestException as e:
#             raise UserError(_("Api Connection Error s%")% str(e))
            