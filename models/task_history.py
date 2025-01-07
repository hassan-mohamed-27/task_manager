from odoo import models, fields, api

class TaskHistory(models.Model):
    """
    Task History Model
    
    This model tracks the history of state changes for tasks. It maintains a chronological
    record of when tasks transition between states and who made the changes.
    
    Each record represents a single state transition and includes:
    - The task being tracked
    - The user who made the change
    - The old and new states
    - The timestamp of the change
    """
    _name = 'task.history'
    _description = 'Task State History'
    _order = 'sequence desc, date desc'
    _rec_name = "sequence"

    sequence = fields.Char(
        string='Sequence',
        readonly=True,
        help="Task sequence number for reference"
    )
    
    task_id = fields.Many2one(
        'task.manager',
        string='Task',
        required=True,
        ondelete='cascade',
        index=True,
        help="Reference to the task being tracked"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Changed By',
        required=True,
        default=lambda self: self.env.user,
        index=True,
        help="User who made the state change"
    )
    
    date = fields.Datetime(
        string='Change Date',
        default=fields.Datetime.now,
        required=True,
        index=True,
        help="Date and time when the state change occurred"
    )
    
    old_state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ],
        string='Previous State',
        index=True,
        help="State of the task before the change"
    )
    
    new_state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ],
        string='New State',
        required=True,
        index=True,
        help="State of the task after the change"
    )
  
    is_latest = fields.Boolean(
        string='Is Latest',
        compute='_compute_is_latest',
        store=True,
        help="Indicates if this is the most recent state change"
    )

   
