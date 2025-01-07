from odoo.tests.common import TransactionCase
from datetime import datetime

class TestTaskHistory(TransactionCase):

    def setUp(self):
        super(TestTaskHistory, self).setUp()
        self.task_obj = self.env['task.manager']
        self.history_obj = self.env['task.history']
        self.user_obj = self.env['res.users']
        
        # Create test user and get its partner
        self.test_user = self.user_obj.create({
            'name': 'History Test User',
            'login': 'history.test@example.com',
            'email': 'history.test@example.com',
        })
        self.test_partner = self.test_user.partner_id
        
        # Create test task
        self.test_task = self.task_obj.create({
            'name': 'History Test Task',
            'description': 'Task for History Testing',
            'state': 'draft',
            'user_id': [(4, self.test_partner.id)],
        })

    def test_history_creation(self):
        """Test history record creation on state change"""
        # Change task state
        self.test_task.state = 'in_progress'
        
        # Check if history record was created
        history = self.history_obj.search([
            ('task_id', '=', self.test_task.id),
            ('old_state', '=', 'draft'),
            ('new_state', '=', 'in_progress')
        ])
        self.assertTrue(history)
        self.assertEqual(len(history), 1)
        self.assertEqual(history.user_id.id, self.env.uid)

    def test_multiple_state_changes(self):
        """Test multiple state changes history"""
        # First state change
        self.test_task.state = 'in_progress'
        
        # Second state change
        self.test_task.state = 'done'
        
        # Check history records
        history_records = self.history_obj.search([
            ('task_id', '=', self.test_task.id)
        ])
        self.assertEqual(len(history_records), 2)
        
        # Check the order of changes
        sorted_history = history_records.sorted('date')
        self.assertEqual(sorted_history[0].old_state, 'draft')
        self.assertEqual(sorted_history[0].new_state, 'in_progress')
        self.assertEqual(sorted_history[1].old_state, 'in_progress')
        self.assertEqual(sorted_history[1].new_state, 'done') 