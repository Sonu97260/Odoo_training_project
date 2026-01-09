from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class ProjectTaskEndWizard(models.TransientModel):
    _name = 'project.task.end.wizard'
    _description = 'Project Task End Wizard'

    task_timer_id = fields.Many2one('project.task.timer', string='Timer', required=True)
    task_description = fields.Text(string='Enter Task Description')
    
    start_date = fields.Datetime(
        string='Start Date',
        related='task_timer_id.start_time',  # already correct
        readonly=True
    )
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now, readonly=True)
    duration = fields.Char(string='Duration (HH:MM)', compute='_compute_duration')

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                diff = record.end_date - record.start_date
                total_seconds = int(diff.total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                record.duration = f"{hours:02}:{minutes:02}"
            else:
                record.duration = "00:00"


    def action_end_task(self):
        self.ensure_one()
        
        # Ensure we use the exact current time for accurate duration
        self.end_date = fields.Datetime.now()
        
        # Call standard action_timer_stop to clear base timer state and create standard timesheet
        try:
            res = self.task_timer_id.task_id.action_timer_stop()
            logger.info("ACTION TIMER STOP RESULT: %s", res)
            
            # Automate standard wizard if returned
            if res and isinstance(res, dict) and res.get('res_model') == 'hr.timesheet.stop.timer.confirmation.wizard':
                logger.info("Standard wizard detected. Attempting auto-confirmation.")
                ctx = res.get('context', {})
                wiz = self.env[res['res_model']].sudo().with_context(ctx).create({})
                
                # Try the discovered confirmation method
                confirmed = False
                
                # Based on introspection: 'action_save_timesheet' is the key method
                target_methods = ['action_save_timesheet', 'action_confirm', 'save', 'confirm']
                
                for method in target_methods:
                    if hasattr(wiz, method):
                        try:
                            getattr(wiz, method)()
                            logger.info("Successfully executed wizard method: %s", method)
                            confirmed = True
                            break
                        except Exception as e:
                            logger.warning("Failed to execute wizard method %s: %s", method, e)
                
                if not confirmed:
                    logger.warning("Could not find suitable confirmation method on standard wizard.")
                
                if not confirmed:
                    logger.warning("Could not find confirmation method on standard wizard.")
                    
        except AttributeError:
            logger.warning("Standard action_timer_stop not found.")

        # Calculate unit_amount in hours (for custom record or fallback)
        duration_seconds = (self.end_date - self.start_date).total_seconds()
        unit_amount = duration_seconds / 3600.0

        # Find the timesheet created by action_timer_stop (recently created for this task/user)
        # We update it with our description.
        # If action_timer_stop didn't create one (e.g. error or different flow), we create one.
        recent_timesheet = self.env['account.analytic.line'].search([
            ('task_id', '=', self.task_timer_id.task_id.id),
            ('user_id', '=', self.task_timer_id.user_id.id),
            ('create_date', '>=', fields.Datetime.now() - timedelta(minutes=1)) # Created just now
        ], order='create_date desc', limit=1)

        if recent_timesheet:
            recent_timesheet.write({
                'name': self.task_description or '/',
                'unit_amount': unit_amount, # Ensure duration matches our calculation
            })
            
            # FORCE STOP: Ensure any timer_start field is cleared on the timesheet line itself
            # This handles cases where the standard action_timer_stop failed to update the line
            try:
                recent_timesheet.write({'timer_start': False})
            except Exception:
                pass
        else:
            # Fallback: Create timesheet entry manually if standard default didn't
            self.env['account.analytic.line'].create({
                'name': self.task_description or '/',
                'project_id': self.task_timer_id.project_id.id,
                'task_id': self.task_timer_id.task_id.id,
                'date': fields.Date.context_today(self),
                'unit_amount': unit_amount,
                'user_id': self.task_timer_id.user_id.id,
                'employee_id': self.env['hr.employee'].search([('user_id', '=', self.task_timer_id.user_id.id)], limit=1).id,
            })
            
        # Clean up ANY "stuck" timesheet lines for this user/task (Running timers might have unit_amount > 0)
        # We look for any recent lines (last 30 days) to be safe
        potential_running_lines = self.env['account.analytic.line'].search([
            ('task_id', '=', self.task_timer_id.task_id.id),
            ('user_id', '=', self.task_timer_id.user_id.id),
            ('date', '>=', fields.Date.context_today(self) - timedelta(days=30)),
        ])
        
        # Field Introspection Results:
        # timer_start, timer_pause, is_timer_running
        timer_fields = ['timer_start', 'timer_pause']

        for line in potential_running_lines:
            for field_name in timer_fields:
                try:
                    if line[field_name]:
                        line.sudo().write({field_name: False})
                        logger.info("Force stopped timer by clearing field '%s' on line %s", field_name, line.id)
                except Exception as e:
                    logger.warning("Could not clear field '%s' on line %s: %s", field_name, line.id, e)
            
            # Ensure 'unit_amount' is updated if we matched the recent line
            if recent_timesheet and line.id == recent_timesheet.id:
                 pass # Already set above
            elif line.unit_amount == 0 and unit_amount > 0:
                 # If we found a 0-hour ghost line, maybe set the time?
                 # Better to leave it 0 hour but STOPPED.
                 pass

        self.task_timer_id.write({
            'start_time': self.start_date,
            'end_date': self.end_date,
            'description': self.task_description,
            'is_running': False,
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'reload_view_timer',
        }
