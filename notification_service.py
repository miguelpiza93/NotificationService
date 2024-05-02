from collections import defaultdict
from datetime import datetime, timedelta


class NotificationService:
    def __init__(self):
        self.rate_limits = {
            "Status": {"interval": timedelta(minutes=1), "limit": 2},
            "News": {"interval": timedelta(days=1), "limit": 1},
            "Marketing": {"interval": timedelta(hours=1), "limit": 3},
        }
        self.notification_time_by_recipient = defaultdict(lambda: defaultdict(list))

    def send_notification(self, recipient, notification_type):

        if notification_type not in self.rate_limits:
            print("Not allowed notification type.")
            return False

        limit_info = self.rate_limits[notification_type]
        interval = limit_info["interval"]
        limit = limit_info["limit"]

        notification_times = self.notification_time_by_recipient[recipient][notification_type]

        if len(notification_times) < limit:
            self.add_notification(recipient, notification_type)
            return True

        now = datetime.now()
        oldest_notification = notification_times[0]
        if now - oldest_notification < interval:
            print(f"Reached limit for {notification_type} - {recipient}.")
            return False

        self.remove_oldest_notification(recipient, notification_type)
        self.add_notification(recipient, notification_type)
        return True

    def add_notification(self, recipient, notification_type):
        self.notification_time_by_recipient[recipient][notification_type].append(datetime.now())

    def remove_oldest_notification(self, recipient, notification_type):
        notification_times = self.notification_time_by_recipient[recipient][notification_type]
        del notification_times[0]
