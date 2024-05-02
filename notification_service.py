from collections import defaultdict
from datetime import datetime, timedelta

from notification_type import NotificationType


class NotificationService:
    __RATE_LIMITS = {
        NotificationType.STATUS: {"interval": timedelta(minutes=1), "limit": 2},
        NotificationType.NEWS: {"interval": timedelta(days=1), "limit": 1},
        NotificationType.MARKETING: {"interval": timedelta(hours=1), "limit": 3},
    }

    def __init__(self):
        self.__notification_time_by_recipient = defaultdict(lambda: defaultdict(list))

    def send_notification(self, recipient: str, notification_type: NotificationType) -> bool:

        if notification_type not in self.__RATE_LIMITS:
            print("Not allowed notification type.")
            return False

        limit_info = self.__RATE_LIMITS[notification_type]
        interval = limit_info["interval"]
        limit = limit_info["limit"]

        notification_times = self.__notification_time_by_recipient[recipient][notification_type]

        if len(notification_times) < limit:
            self.__add_notification(recipient, notification_type)
            return True

        oldest_notification = notification_times[0]
        time_since_oldest_notification = datetime.now() - oldest_notification
        if time_since_oldest_notification < interval:
            print(f"Reached limit for {notification_type.value} - {recipient}.")
            return False

        self.__remove_oldest_notification(recipient, notification_type)
        self.__add_notification(recipient, notification_type)
        return True

    def __add_notification(self, recipient, notification_type):
        self.__notification_time_by_recipient[recipient][notification_type].append(datetime.now())

    def __remove_oldest_notification(self, recipient, notification_type):
        notification_times = self.__notification_time_by_recipient[recipient][notification_type]
        del notification_times[0]
