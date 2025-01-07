# -*- coding: utf-8 -*-
{
    'name': 'Task Manager',
    'version': '17.0.0.1.0',
    'category': 'Project',
    'summary': 'Task Management System',
    'description': """
        Task Management System for Odoo
        =============================
        
        A comprehensive task management system that provides:
        
        Features:
        ---------
        * Create and manage tasks with detailed information
        * Track task progress and state changes
        * Assign tasks to multiple users
        * Color-coded task status based on deadlines
        * Detailed task history tracking
        * Progress entry logging
        
        Views:
        ------
        * Kanban view with drag-and-drop functionality
        * Detailed form view with chatter integration
        * List view for task overview
        * Search view with filters and grouping
        
        Reports:
        --------
        * Task progress reports
        * State change history
        
        API Integration:
        ---------------
        * RESTful API endpoints for external integration
        * CRUD operations for tasks
        * Progress and history tracking endpoints
        
        Technical Details:
        ----------------
        * Built for Odoo 17.0
        
        
    """,
    
    'author': 'hassan',

    
    'depends': [
        'base',
        'contacts',
        'mail',
        
    ],
    
    'data': [
        'security/ir.model.access.csv',
        'views/task_management_view.xml',
        'views/task_history_views.xml',
        'views/user_task_view.xml',
        'views/task_sequence.xml',
        'data/cron.xml',
        'reports/task_progress_report.xml',
    ],
    
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    
    
    
    
   
}
