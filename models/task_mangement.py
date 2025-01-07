from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date

class Task(models.Model):
    """
    Task Management Model
    
    This model represents the core task management functionality. It handles task creation,
    state management, progress tracking, and task history. Tasks can be assigned to users,
    tracked through different states, and monitored for progress.
    
    Inherits:
        - mail.thread: For message and notification handling
        - mail.activity.mixin: For activity management
    """
    _name = 'task.manager'
    _description = 'Task Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    # Relationships
    progress_ids = fields.One2many(
        'task.progress',
        'task_id',
        string='Progress Entries',
        help="Track detailed progress entries for this task"
    )
    
    history_ids = fields.One2many(
        'task.history', 
        'task_id', 
        string='State History',
        help="Historical record of state changes"
    )

    # Basic Fields
    name = fields.Char(
        string='Task Name',
        required=True,
        tracking=True,
        help="Name of the task"
    )
    description = fields.Text(
        string='Description',
        tracking=True,
        help="Detailed description of the task"
    )
    start_date = fields.Date(
        string='Start Date',
        default=fields.Date.today,
        tracking=True,
        help="Task start date"
    )
    end_date = fields.Date(
        string='End Date',
        tracking=True,
        help="Expected completion date"
    )
    user_id = fields.Many2many(
        'res.partner',
        string='Assigned to',
        tracking=True,
        help="Users assigned to this task"
    )
    
    # State Management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ],
        string='Status',
        default='draft',
        tracking=True,
        group_expand='_expand_states',
        help="Current state of the task"
    )
    
    # Task Identification
    sequence_number = fields.Char(
        string='Task Sequence',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: self.env['ir.sequence'].sudo().next_by_code('task.manager.sequence') or _('New'),
        help="Unique identifier for the task"
    )

    # Visual Indicators
    task_color = fields.Selection([
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('red', 'Red'),
        ('orange', 'Orange')
    ],
        string='Task Color',
        default='blue',
        help="Color indicator for task status and urgency"
    )
    
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        help="Task creation/modification date"
    )

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """
        Validate that end date is after start date.
        
        Raises:
            ValidationError: If end date is before start date
        """
        for task in self:
            if task.start_date and task.end_date and task.start_date > task.end_date:
                raise ValidationError('End date must be after start date')

    def action_in_progress(self):
        """
        Move task to in progress state.
        This method updates the task state and triggers history tracking.
        """
        for task in self:
            task.write({'state': 'in_progress'})

    def action_done(self):
        """
        Mark task as done.
        This method updates the task state and triggers history tracking.
        """
        for task in self:
            task.write({'state': 'done'})

    @api.model
    def update_task_colors(self):
        """
        Update task colors based on their deadline status.
        
        Color coding:
        - Green: Task is done
        - Red: Task is overdue
        - Orange: Task is due within 2 days
        - Blue: Default color
        
        Returns:
            bool: True if colors were updated successfully
        """
        today = date.today()
        tasks = self.search([])
        
        for task in tasks:
            if task.state == 'done':
                task.task_color = 'green'
            elif task.end_date:
                if task.end_date < today:
                    task.task_color = 'red'
                elif (task.end_date - today).days <= 2:
                    task.task_color = 'orange'
                else:
                    task.task_color = 'blue'
            else:
                task.task_color = 'blue'
        return True

    @api.model
    def _update_task_colors(self):
        """
        Cron job method to automatically update task colors.
        This method is called by the scheduled action.
        """
        self.with_context(from_compute=False).update_task_colors()

    @api.model
    def _expand_states(self, states, domain, order):
        """
        Helper method for kanban view to show all states.
        
        Returns:
            list: List of all possible states
        """
        return [key for key, val in self._fields['state'].selection]

  
   
    def write(self, vals):
        """
        Override write method to track state changes.
        Creates a history record when task state changes.
        
        Args:
            vals (dict): The values to write
            
        Returns:
            bool: True if write was successful
        """
        if 'state' in vals:
            for record in self:
                self.env['task.history'].create({
                    'task_id': record.id,
                    'old_state': record.state,
                    'new_state': vals['state'],
                    'sequence': record.sequence_number
                })
        return super(Task, self).write(vals)

    def action_view_history(self):
        """
        Smart button action to view task history.
        
        Returns:
            dict: Action dictionary to open history view
        """
        self.ensure_one()
        return {
            'name': _('Task History'),
            'type': 'ir.actions.act_window',
            'res_model': 'task.manager',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(self.env.ref('task_manger.view_task_state_history_form').id, 'form')],
            'target': 'current',
        }

    def action_view_task(self):
        """
        Smart button action to view task form.
        
        Returns:
            dict: Action dictionary to open task form view
        """
        self.ensure_one()
        return {
            'name': _('Task'),
            'type': 'ir.actions.act_window',
            'res_model': 'task.manager',
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(self.env.ref('task_manger.view_task_manager_form').id, 'form')],
            'target': 'current',
        }