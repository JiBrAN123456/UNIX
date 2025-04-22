from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task, User

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
