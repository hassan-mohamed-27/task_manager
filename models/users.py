from odoo import models, fields

class ResPartner(models.Model):
    """
    Extension of the Partner Model for Task Management
    
    This model extends the base res.partner model to add task management
    related fields and functionality. It allows tracking of tasks assigned
    to partners/users.
    """
    _inherit = 'res.partner'

    task_ids = fields.Many2many(
        'task.manager',
        string='Tasks',
        help="Tasks assigned to this partner"
    )