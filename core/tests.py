from django.test import TestCase
from django.contrib.auth.models import User
from .models import Member


class MemberTestCase(TestCase):

    def setUp(self):
        good_user = User.objects.create_user("good", email="someone@gmail.com")
        missing_user = User.objects.create_user("missing")
        bad_user = User.objects.create_user("bad", email="bogus")
        fake_user = User.objects.create_user("fake", email="someone@fake.com")
        Member.objects.create(user=good_user, ghin="123")
        Member.objects.create(user=missing_user, ghin="456")
        Member.objects.create(user=bad_user, ghin="654")
        Member.objects.create(user=fake_user, ghin="789")

    def test_good_user_has_email(self):
        member = Member.objects.get(ghin="123")
        self.assertTrue(member.has_email())

    def test_missing_user_has_email(self):
        member = Member.objects.get(ghin="456")
        self.assertFalse(member.has_email())

    def test_bad_user_has_email(self):
        member = Member.objects.get(ghin="654")
        self.assertFalse(member.has_email())

    def test_fake_user_has_email(self):
        member = Member.objects.get(ghin="789")
        self.assertFalse(member.has_email())
