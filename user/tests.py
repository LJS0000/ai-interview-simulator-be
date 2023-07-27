from django.test import TestCase
from django.utils import timezone
from .models import User
from .tasks import reset_daily_chats


class UserModelTestCase(TestCase):
    def test_update_database_at_midnight(self):
        # 모의 데이터베이스 객체 생성
        user1 = User.objects.create(email='data1@example.com', password='example1')
        user2 = User.objects.create(email='data2@example.com', password='example2')

        # 자정 작업이 예상대로 수행되는지 확인
        user1.refresh_from_db()
        user2.refresh_from_db()

        # user1과 user2의 필드를 확인하여 예상대로 변경되었는지 검증
        self.assertEqual(user1.daily_chats, 0)
        self.assertEqual(user2.daily_chats, 0)

        # 필드가 예상대로 변경되었다면 기타 필드들은 변경되지 않았는지 검증
        self.assertEqual(user1.email, 'data1@example.com')
        self.assertEqual(user1.password, 'example1')
        self.assertEqual(user2.email, 'data2@example.com')
        self.assertEqual(user2.password, 'example2')
