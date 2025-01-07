# -*- coding: utf-8 -*-
from odoo import models, api

class TaskProgressReport(models.AbstractModel):
    """
    Task Progress Report Model
    
    This model generates detailed progress reports for tasks. It provides
    the business logic for the task progress report template, formatting
    and calculating data for presentation in the report.
    """
    _name = 'report.task_manger.task_progress_report'
    _description = 'Task Progress Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Prepare values for report rendering.
        
        Args:
            docids: List of document IDs
            data: Additional report data
            
        Returns:
            dict: Values for report template rendering
        """
        docs = self.env['task.manager'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'task.manager',
            'docs': docs,
        } 