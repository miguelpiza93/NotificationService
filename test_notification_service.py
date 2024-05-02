import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from notification_service import NotificationService


class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.notification_service = NotificationService()

    def test_status_limit(self):
        for _ in range(2):
            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertTrue(result)
        result = self.notification_service.send_notification("user1@example.com", "Status")
        self.assertFalse(result)

    def test_status_limit_different_recipient(self):
        for _ in range(2):
            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertTrue(result)
        result = self.notification_service.send_notification("user2@example.com", "Status")
        self.assertTrue(result)

    def test_status_limit_time_interval(self):
        now = datetime(2024, 5, 1, 14, 10, 0)

        with patch('notification_service.datetime') as mock_datetime:
            mock_datetime.now.return_value = now

            # First notification sent at 14:10.0
            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertTrue(result)

            future_time = now + timedelta(seconds=30)
            mock_datetime.now.return_value = future_time

            # Second notification sent at 14:10.30
            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertTrue(result)

            future_time = now + timedelta(seconds=60)
            mock_datetime.now.return_value = future_time

            # 1 min after first notification
            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertTrue(result)

            future_time = now + timedelta(seconds=80)
            mock_datetime.now.return_value = future_time

            # 14:11.20, Missing 10 seconds to be able to send a new notification
            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertFalse(result)

            # 14:11.30, Ready to send a new notification
            future_time = now + timedelta(seconds=90)
            mock_datetime.now.return_value = future_time

            result = self.notification_service.send_notification("user1@example.com", "Status")
            self.assertTrue(result)

    def test_news_limit(self):
        result = self.notification_service.send_notification("user1@example.com", "News")
        self.assertTrue(result)
        result = self.notification_service.send_notification("user1@example.com", "News")
        self.assertFalse(result)

    def test_news_limit_time_interval(self):
        now = datetime.now()

        with patch('notification_service.datetime') as mock_datetime:
            mock_datetime.now.return_value = now

            result = self.notification_service.send_notification("user1@example.com", "News")
            self.assertTrue(result)

            future_time = now + timedelta(days=1)
            mock_datetime.now.return_value = future_time

            result = self.notification_service.send_notification("user1@example.com", "News")
            self.assertTrue(result)

    def test_marketing_limit(self):
        for _ in range(3):
            result = self.notification_service.send_notification("user1@example.com", "Marketing")
            self.assertTrue(result)
        result = self.notification_service.send_notification("user1@example.com", "Marketing")
        self.assertFalse(result)

    def test_unsupported_notification(self):
        result = self.notification_service.send_notification("user1@example.com", "InvalidType")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
