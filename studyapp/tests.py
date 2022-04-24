import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Meeting

# Create your tests here.

# class MeetingModelTests(TestCase):
#
#     def test_was_posted_recently_with_future_meeting(self):
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_meeting = Meeting(post_date=time)
#         self.assertIs(future_meeting.was_posted_recently(), False)
#
#     def test_was_posted_recently_with_old_meeting(self):
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         old_meeting = Meeting(post_date=time)
#         self.assertIs(old_meeting.was_posted_recently(), False)
#
#     def test_was_posted_recently_with_recent_meeting(self):
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         recent_meeting = Meeting(post_date=time)
#         self.assertIs(recent_meeting.was_posted_recently(), True)
#
# def create_meeting(post_text, days):
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Meeting.objects.create(post_text=post_text, post_date=time)
#
# class MeetingIndexViewTests(TestCase):
#
#     def test_no_meetings(self):
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No meetings are available.")
#         self.assertQuerysetEqual(response.context['latest_reply_list'], [])
#
#     def test_past_meeting(self):
#         meeting = create_meeting(post_text="Past meeting.", days=-30)
#         response = self.client.get(reverse('index'))
#         self.assertQuerysetEqual(response.context['latest_reply_list'], [meeting])
#
#     def test_future_meeting(self):
#         create_meeting(post_text="Future meeting.", days=30)
#         response = self.client.get(reverse('index'))
#         self.assertContains(response, "No meetings are available.")
#         self.assertQuerysetEqual(response.context['latest_reply_list'], [])
#
#     def test_future_meeting_and_past_meeting(self):
#         meeting = create_meeting(post_text="Past meeting.", days=-30)
#         create_meeting(post_text="Future meeting.", days=30)
#         response = self.client.get(reverse('index'))
#         self.assertQuerysetEqual(response.context['latest_reply_list'], [meeting])
#
#     def test_two_past_meetings(self):
# 	    meeting1 = create_meeting(post_text="Past meeting 1.", days=-30)
# 	    meeting2 = create_meeting(post_text="Past meeting 2.", days=-5)
# 	    response = self.client.get(reverse('index'))
# 	    self.assertQuerysetEqual(response.context['latest_reply_list'], [meeting2, meeting1])
#
# class MeetingDetailViewTests(TestCase):
#
#     def test_future_meeting(self):
#         future_meeting = create_meeting(post_text='Future Meeting.', days=5)
#         url = reverse('detail', args=(future_meeting.id,))
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 404)
#
#     def test_past_meeting(self):
#         past_meeting = create_meeting(post_text='Past Meeting.', days=-5)
#         url = reverse('detail', args=(past_meeting.id,))
#         response = self.client.get(url)
#         self.assertContains(response, past_meeting.post_text)
