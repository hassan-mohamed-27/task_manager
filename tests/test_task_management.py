from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestTaskManagement(TransactionCase):

    def setUp(self):
        super(TestTaskManagement, self).setUp()
        self.task_obj = self.env['task.manager']
        self.user_obj = self.env['res.users']
        
        # Create test user and get its partner
        self.test_user = self.user_obj.create({
            'name': 'Test User',
            'login': 'test.user@example.com',
            'email': 'test.user@example.com',
        })
        self.test_partner = self.test_user.partner_id

    def test_create_task(self):
        """Test task creation"""
        task = self.task_obj.create({
            'name': 'Test Task',
            'description': 'Test Description',
            'state': 'draft',
            'user_id': [(4, self.test_partner.id)],
            'start_date': datetime.now().date(),
            'end_date': (datetime.now() + timedelta(days=5)).date(),
        })
        self.assertEqual(task.name, 'Test Task')
        self.assertEqual(task.state, 'draft')
        self.assertIn(self.test_partner, task.user_id)

    def test_task_state_transition(self):
        """Test task state transitions"""
        task = self.task_obj.create({
            'name': 'State Test Task',
            'description': 'Testing State Transitions',
            'state': 'draft',
            'user_id': [(4, self.test_partner.id)],
        })
        
        # Test transition to in_progress
        task.state = 'in_progress'
        self.assertEqual(task.state, 'in_progress')
        
        # Test transition to done
        task.state = 'done'
        self.assertEqual(task.state, 'done')

    def test_task_deadline_validation(self):
        """Test task deadline validation"""
        with self.assertRaises(ValidationError):
            self.task_obj.create({
                'name': 'Past Deadline Task',
                'description': 'Task with past deadline',
                'state': 'draft',
                'user_id': [(4, self.test_partner.id)],
                'start_date': datetime.now().date(),
                'end_date': (datetime.now() - timedelta(days=1)).date(),
            }) 