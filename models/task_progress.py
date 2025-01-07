from odoo import models, fields, api

class TaskProgress(models.Model):
    """
    Task Progress Model
    
    This model tracks detailed progress entries for tasks. It allows users to log
    their work and progress updates on specific tasks. Each entry includes the user,
    date, and description of work performed.
    """
    _name = 'task.progress'
    _description = 'Task Progress Entry'
    _order = 'date desc'

    task_id = fields.Many2one(
        'task.manager',
        string='Task',
        required=True,
        ondelete='cascade',
        help="The task this progress entry belongs to"
    )

    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        default=lambda self: self.env.user,
        help="User who logged this progress entry"
    )

    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        required=True,
        help="Date and time when this progress was logged"
    )

    work_description = fields.Text(
        string='Work Description',
        required=True,
        help="Description of work done or progress made"
    )

    user_domain = fields.Char(
        compute='_compute_user_domain',
        help="Technical field to filter users based on task assignment"
    )

    @api.depends('task_id')
    def _compute_user_domain(self):
        """
        Compute method to set the domain for user selection.
        Filters users based on task assignment.
        """
        for record in self:
            record.user_domain = "[('id', 'in', %s)]" % str(record.task_id.user_id.ids) 