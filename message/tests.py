from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Message, Chat_room

class SendMessageAPITest(APITestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver1 = User.objects.create_user(username='bob', password='password123')
        self.receiver2 = User.objects.create_user(username='charlie', password='password123')

        # Create a chat room
        self.chat_room = Chat_room.objects.create(name='Test Room')

        # URL of the send_message view
        self.url = reverse('send_message')

        # Valid message payload
        self.valid_payload = {
            "sender": self.sender.id,
            "receiver": [self.receiver1.id, self.receiver2.id],
            "content": "Hello everyone!",
            "chat_room": self.chat_room.id
        }

        # Invalid message payload (missing content)
        self.invalid_payload = {
            "sender": self.sender.id,
            "receiver": [self.receiver1.id],
            "content": "",
            "chat_room": self.chat_room.id
        }

    def test_send_message_success(self):
        """Test that a valid message is created successfully"""
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Message sent successfully')

        # Check that the message is stored in the database
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.sender, self.sender)
        self.assertIn(self.receiver1, message.receiver.all())
        self.assertIn(self.receiver2, message.receiver.all())
        self.assertEqual(message.content, "Hello everyone!")
        self.assertEqual(message.chat_room, self.chat_room)

    def test_send_message_invalid(self):
        """Test that invalid data returns 400"""
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)


class LoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

class LogoutAPITest(APITestCase):
    def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='testpass')
            self.login_url = reverse('login')
            self.logout_url = reverse('logout')

    def test_logout_success(self):
            # Login to get token
            login_response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
            token = login_response.data.get('token')
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            # Logout with token
            response = self.client.post(self.logout_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalid(self):
            # No token — unauthorized
            response = self.client.post(self.logout_url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)