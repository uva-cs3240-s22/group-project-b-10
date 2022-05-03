import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Meeting, Room, Profile, User, Friend_Request, Course

# Create your tests here.

class MeetingModelTests(TestCase):

    def test_was_posted_recently_with_future_meeting(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_meeting = Meeting(post_date=time)
        self.assertIs(future_meeting.was_posted_recently(), False)

    def test_was_posted_recently_with_old_meeting(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_meeting = Meeting(post_date=time)
        self.assertIs(old_meeting.was_posted_recently(), False)

    def test_was_posted_recently_with_recent_meeting(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_meeting = Meeting(post_date=time)
        self.assertIs(recent_meeting.was_posted_recently(), True)

def create_meeting(post_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Meeting.objects.create(post_text=post_text, post_date=time)

class MeetingIndexViewTests(TestCase):

    def test_no_meetings(self):
        response = self.client.get(reverse('browse-meetings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No meetings are available.")
        self.assertQuerysetEqual(response.context['latest_reply_list'], [])

    def test_future_meeting(self):
        create_meeting(post_text="Future meeting.", days=30)
        response = self.client.get(reverse('browse-meetings'))
        self.assertContains(response, "No meetings are available.")
        self.assertQuerysetEqual(response.context['latest_reply_list'], [])


class ProfileTest(TestCase):
    def user_equals_profile(self):
        test_user = User.objects.create(
            first_name = "Jim",
            last_name = "Halpert",
            email = "dundermifflin@gmail.com"
        )
        target_profile = Profile.objects.get(name = "Jim Halpert")
        profiles = Profile.objects.all()
        self.assertContains(target_profile, profiles)

# class HomePageTest(TestCase):
#     def test_all_rooms_are_rendered_in_homepage(self):
#         Room.objects.create(
#             name='room 1',
#             slug='room-1',
#             description='This is the 1st room'
#         )
#         Room.objects.create(
#             name='room 2',
#             slug='room-2',
#             description='This is the 2nd room'
#         )
#
#         response = self.client.get('/')
#
#         self.assertContains(response, 'room 1')
#         self.assertContains(response, 'room 2')
#
# class RoomDetailTest(TestCase):
#
#     def test_room_details_are_present_in_room_page(self):
#         room_1 = Room.objects.create(
#             name='room X',
#             slug='room-x',
#             description='This is the X-room'
#         )
#
#         response = self.client.get('/rooms/{}/'.format(room_1.slug))
#
#         self.assertContains(response, room_1.name)
#         self.assertContains(response, room_1.description)

