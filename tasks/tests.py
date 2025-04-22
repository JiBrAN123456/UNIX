from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task, User
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import time

User = get_user_model()


class TaskManagerTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "testuser"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.register_url = reverse('token_obtain_pair')  # JWT login
        self.task_url = reverse('task-list-create')  # tasks/

        # Login and get token
        response = self.client.post(self.register_url, {"username": self.username, "password": self.password})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_task(self):
        response = self.client.post(self.task_url, {"name": "Test Task"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().name, "Test Task")

    def test_list_tasks(self):
        Task.objects.create(user=self.user, name="Sample Task 1")
        Task.objects.create(user=self.user, name="Sample Task 2")

        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_task(self):
        task = Task.objects.create(user=self.user, name="Delete Me")
        delete_url = reverse('task-delete', kwargs={'pk': task.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_filter_task_by_status(self):
        Task.objects.create(user=self.user, name="Running Task", status='running')
        Task.objects.create(user=self.user, name="Completed Task", status='completed')

        response = self.client.get(self.task_url + '?status=completed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'completed')



class TaskAutoCompletionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='auto_user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_task_status_auto_changes_to_completed(self):
        response = self.client.post('/api/tasks/', {'name': 'Auto Status Task'})
        self.assertEqual(response.status_code, 201)

        task_id = response.data['id']

        # Wait for simulated task to complete
        time.sleep(6)  # Ensure it's more than the auto-complete delay (e.g., 5s)

        updated_response = self.client.get(f'/api/tasks/{task_id}/')
        self.assertEqual(updated_response.status_code, 200)
        self.assertEqual(updated_response.data['status'], 'completed')


class TaskDeleteTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='delete_user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_delete_task(self):
        # Create a task
        response = self.client.post('/api/tasks/', {'name': 'Delete Me'})
        task_id = response.data['id']

        # Delete it
        delete_response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(delete_response.status_code, 204)

        # Verify it's deleted
        get_response = self.client.get(f'/api/tasks/{task_id}/')
        self.assertEqual(get_response.status_code, 404)        


class TaskFilterByStatusTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='filter_user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_filter_completed_tasks(self):
        # Create 2 tasks
        self.client.post('/api/tasks/', {'name': 'Task A'})
        self.client.post('/api/tasks/', {'name': 'Task B'})

        # Let them auto-complete
        time.sleep(6)

        # Filter for completed
        response = self.client.get('/api/tasks/?status=completed')
        self.assertEqual(response.status_code, 200)
        for task in response.data:
            self.assertEqual(task['status'], 'completed')



class TaskInvalidInputTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='bad_user', password='test123')
        self.client.force_authenticate(user=self.user)

    def test_create_task_without_name(self):
        response = self.client.post('/api/tasks/', {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('name', response.data)
