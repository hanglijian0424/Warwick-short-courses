import unittest
from app import app
import sqlite3
class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Test client and test environment
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Create test database tables (only in the test environment)
        with sqlite3.connect('internship.db') as conn:
            conn.execute("""
                   CREATE TABLE IF NOT EXISTS applications (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       email TEXT NOT NULL,
                       course_name TEXT NOT NULL,
                       statement TEXT NOT NULL,
                       timestamp TEXT NOT NULL,
                       status TEXT DEFAULT 'pending'
                   );
               """)
            conn.commit()
#This unit test code is written by chatgpt
    def test_homepage_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Warwick Summer Learning', response.data)

    def test_apply_page_loads(self):
        response = self.app.get('/apply')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Apply for a Short Course', response.data)

    def test_admin_redirect_without_login(self):
        response = self.app.get('/admin/dashboard', follow_redirects=True)
        self.assertIn(b'Admin Login', response.data)

    def test_fake_submission(self):
        response = self.app.post('/apply', data={
            'name': 'Test User',
            'email': 'test@example.com',
            'course_name': 'AI and Data Science',
            'statement': 'I want to join this course.'
        }, follow_redirects=True)
        self.assertIn(b'Thank you for your application', response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
