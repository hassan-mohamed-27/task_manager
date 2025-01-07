from odoo import http
from odoo.http import request, Response
import json

class TaskController(http.Controller):
    """
    REST API Controller for Task Management
    
    This controller provides RESTful API endpoints for managing tasks, including:
    - Task CRUD operations
    - Task progress tracking
    - Task history viewing
    
    All endpoints support CORS and return JSON responses.
    Authentication is disabled for demonstration purposes.
    """

    def _format_task_data(self, task):
        """
        Format task data for API response.
        
        Args:
            task: Task record to format
            
        Returns:
            dict: Formatted task data
        """
        return {
            'id': task.id,
            'sequence_number': task.sequence_number,
            'name': task.name,
            'description': task.description,
            'state': task.state,
            'start_date': str(task.start_date) if task.start_date else False,
            'end_date': str(task.end_date) if task.end_date else False,
            'task_color': task.task_color,
            'date': str(task.date) if task.date else False,
            'user_id': [{
                'id': user.id,
                'name': user.name,
            } for user in task.user_id] if task.user_id else []
        }

    def _get_json_data(self):
        """
        Extract JSON data from request.
        
        Returns:
            dict: Parsed JSON data or request parameters
        """
        try:
            return json.loads(request.httprequest.data.decode())
        except:
            return request.params

    def _json_response(self, data, status=200):
        """
        Create JSON response with proper headers.
        
        Args:
            data: Data to return
            status: HTTP status code
            
        Returns:
            Response: HTTP response object
        """
        response = Response(
            json.dumps(data),
            status=status
        )
        response.headers['Content-Type'] = 'application/json'
        return response

    @http.route(['/api/tasks', '/api/tasks/'], type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False)
    def get_tasks(self, **kw):
        """
        Get all tasks.
        
        Returns:
            Response: List of all tasks
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        tasks = request.env['task.manager'].sudo().search([])
        task_list = [self._format_task_data(task) for task in tasks]
        return self._json_response({'status': 'success', 'data': task_list})

    @http.route('/api/tasks/<int:task_id>', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False)
    def get_task(self, task_id, **kw):
        """
        Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve
            
        Returns:
            Response: Task data or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        task = request.env['task.manager'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'status': 'error', 'message': 'Task not found'}, 404)
        return self._json_response({'status': 'success', 'data': self._format_task_data(task)})

    @http.route('/api/tasks', type='http', auth='none', methods=['POST', 'OPTIONS'], csrf=False)
    def create_task(self, **post):
        """
        Create a new task.
        
        Expected POST data:
            name: Task name (required)
            description: Task description (required)
            start_date: Start date (optional)
            end_date: End date (optional)
            task_color: Color code (optional)
            state: Task state (optional)
            user_id: List of user IDs (optional)
            
        Returns:
            Response: Created task data or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        data = self._get_json_data()
        if not data.get('name') or not data.get('description'):
            return self._json_response({'status': 'error', 'message': 'Name and description are required'}, 400)

        vals = {
            'name': data.get('name'),
            'description': data.get('description'),
            'start_date': data.get('start_date', False),
            'end_date': data.get('end_date', False),
            'task_color': data.get('task_color', 'blue'),
            'state': data.get('state', 'draft'),
            
        }

        if data.get('user_id'):
            user_ids = data['user_id']
            if isinstance(user_ids, str):
                user_ids = [int(uid) for uid in user_ids.split(',')]
            elif isinstance(user_ids, int):
                user_ids = [user_ids]
            vals['user_id'] = [(6, 0, user_ids)]

        new_task = request.env['task.manager'].sudo().create(vals)
        return self._json_response({'status': 'success', 'data': self._format_task_data(new_task)})

    @http.route('/api/tasks/<int:task_id>', type='http', auth='none', methods=['PUT', 'OPTIONS'], csrf=False)
    def update_task(self, task_id, **post):
        """
        Update an existing task.
        
        Args:
            task_id: ID of the task to update
            
        Expected PUT data:
            name: Task name (optional)
            description: Task description (optional)
            start_date: Start date (optional)
            end_date: End date (optional)
            task_color: Color code (optional)
            state: Task state (optional)
            user_id: List of user IDs (optional)
            
        Returns:
            Response: Updated task data or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        task = request.env['task.manager'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'status': 'error', 'message': 'Task not found'}, 404)

        data = self._get_json_data()
        vals = {}
        if data.get('name'): vals['name'] = data['name']
        if data.get('description'): vals['description'] = data['description']
        if data.get('start_date'): vals['start_date'] = data['start_date']
        if data.get('end_date'): vals['end_date'] = data['end_date']
        if data.get('task_color'): vals['task_color'] = data['task_color']
        if data.get('state'): vals['state'] = data['state']

        if data.get('user_id'):
            user_ids = data['user_id']
            if isinstance(user_ids, str):
                user_ids = [int(uid) for uid in user_ids.split(',')]
            elif isinstance(user_ids, int):
                user_ids = [user_ids]
            vals['user_id'] = [(6, 0, user_ids)]

        task.write(vals)
        return self._json_response({'status': 'success', 'data': self._format_task_data(task)})

    @http.route('/api/tasks/<int:task_id>', type='http', auth='none', methods=['DELETE', 'OPTIONS'], csrf=False)
    def delete_task(self, task_id, **kw):
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            Response: Success message or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        task = request.env['task.manager'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'status': 'error', 'message': 'Task not found'}, 404)
        task.unlink()
        return self._json_response({'status': 'success', 'message': 'Task deleted successfully'})

    @http.route('/api/tasks/<int:task_id>/progress', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False)
    def get_task_progress(self, task_id, **kw):
        """
        Get progress entries for a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Response: List of progress entries or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        task = request.env['task.manager'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'status': 'error', 'message': 'Task not found'}, 404)

        progress_list = [{
            'id': progress.id,
            'date': str(progress.date),
            'user_id': {
                'id': progress.user_id.id,
                'name': progress.user_id.name
            } if progress.user_id else False,
            'work_description': progress.work_description
        } for progress in task.progress_ids]

        return self._json_response({'status': 'success', 'data': progress_list})

    @http.route('/api/tasks/<int:task_id>/progress', type='http', auth='none', methods=['POST', 'OPTIONS'], csrf=False)
    def add_progress(self, task_id, **post):
        """
        Add a progress entry to a task.
        
        Args:
            task_id: ID of the task
            
        Expected POST data:
            work_description: Description of work done (required)
            user_id: ID of the user making the entry (required)
            date: Date of the progress entry (optional)
            
        Returns:
            Response: Created progress entry or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        task = request.env['task.manager'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'status': 'error', 'message': 'Task not found'}, 404)

        data = self._get_json_data()
        if not data.get('work_description') or not data.get('user_id'):
            return self._json_response({'status': 'error', 'message': 'Work description and user_id are required'}, 400)

        vals = {
            'task_id': task_id,
            'work_description': data['work_description'],
            'user_id': int(data['user_id']),
            'date': data.get('date', False),
        }

        progress = request.env['task.progress'].sudo().create(vals)
        return self._json_response({
            'status': 'success',
            'data': {
                'id': progress.id,
                'date': str(progress.date),
                'work_description': progress.work_description,
                'user_id': {
                    'id': progress.user_id.id,
                    'name': progress.user_id.name
                } if progress.user_id else False
            }
        })

    @http.route('/api/tasks/<int:task_id>/history', type='http', auth='none', methods=['GET', 'OPTIONS'], csrf=False)
    def get_task_history(self, task_id, **kw):
        """
        Get state change history for a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Response: List of state changes or error message
        """
        if request.httprequest.method == 'OPTIONS':
            return self._json_response({})
        task = request.env['task.manager'].sudo().browse(task_id)
        if not task.exists():
            return self._json_response({'status': 'error', 'message': 'Task not found'}, 404)

        history_list = [{
            'id': history.id,
            'sequence': history.sequence,
            'date': str(history.date),
            'old_state': history.old_state,
            'new_state': history.new_state,
            'user_id': {
                'id': history.user_id.id,
                'name': history.user_id.name
            } if history.user_id else False
        } for history in task.history_ids]

        return self._json_response({'status': 'success', 'data': history_list})
