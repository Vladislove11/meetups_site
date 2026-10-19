from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import Meetup, Location, Participant


class IndexViewTest(TestCase):
    def test_index_page_works(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetups/index.html")

    def test_index_shows_meetup(self):
        location = Location.objects.create(name="Москва", address="Красная площадь, 1")
        Meetup.objects.create(
            title="Митап 1",
            slug="meetup-1",
            description="Описание",
            location=location
        )
        response = self.client.get(reverse("index"))
        self.assertContains(response, "Митап 1")
        self.assertContains(response, "meetup-1")

    def test_index_search(self):
        location = Location.objects.create(name="Москва", address="Красная площадь, 1")
        Meetup.objects.create(title="Python Meetup", slug="pythom-meetup", description="тут что то написано", location=location)
        Meetup.objects.create(title="Django Meetup", slug="django-meetup", description="тут опять что то написнао", location=location)

        response = self.client.get(reverse("index"), {"q": "Python"})
        self.assertContains(response, "Python Meetup")
        self.assertNotContains(response, "Django Meetup")

class MeetupDetailViewTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Москва", address="красная площадь, 1")
        self.meetup = Meetup.objects.create(
            title="Тестовый митап",
            slug="test-meetup",
            description="Описание",
            location=self.location
        )
        self.user = User.objects.create_user(username="testuser", password="test123")

    def test_detail_requires_login(self):
        response = self.client.get(reverse("meetup-detail", args=["test-meetup"]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_detail_page_works_authenticated(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("meetup-detail", args=["test-meetup"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetups/meetup-details.html")
        self.assertContains(response, "Тестовый митап")

    def test_detail_404_for_nonexistent(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.get(reverse("meetup-detail", args=["nonexistent"]))
        self.assertEqual(response.status_code, 404)

    def test_register_for_meetup(self):
        self.client.login(username="testuser", password="test123")
        response = self.client.post(reverse("meetup-detail", args=["test-meetup"]), {"action": "register"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.meetup.participants.count(), 1)

    def test_unregister_from_meetup(self):
        self.client.login(username="testuser", password="test123")
        self.client.post(reverse("meetup-detail", args=["test-meetup"]),
                         {"action": "register"})
        self.assertEqual(self.meetup.participants.count(),1)
        self.client.post(reverse("meetup-detail", args=["test-meetup"]),
                         {"action": "unregister"})
        self.assertEqual(self.meetup.participants.count(), 0)

class EditMeetupViewTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Москва", address="Красная площадь, 1")
        self.author = User.objects.create_user(username="author", password="test123")
        self.other_user = User.objects.create_user(username="other", password="test123")
        self.meetup = Meetup.objects.create(
            title="Тестовый митап",
            slug="test-meetup",
            description="Описание",
            location=self.location,
            creator=self.author
        )

    def test_edit_requires_login(self):
        response = self.client.get(reverse("edit-meetup", args=["test-meetup"]))
        self.assertEqual(response.status_code, 302)

    def test_author_can_edit(self):
        self.client.login(username="author", password="test123")
        response = self.client.get(reverse("edit-meetup", args=["test-meetup"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meetups/edit-meetup.html")

    def test_non_author_gets_403(self):
        self.client.login(username="other", password="test123")
        response = self.client.get(reverse("edit-meetup", args=["test-meetup"]))
        self.assertEqual(response.status_code, 403)

    def test_author_can_save_changes(self):
        self.client.login(username="author", password="test123")
        response = self.client.post(
            reverse("edit-meetup", args=["test-meetup"]),
            {
                "title": "Обнавлённый митап",
                "slug": "test-meetup",
                "description": "Новое описание",
                "location": self.location.id,
                "organizer-email": "",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.meetup.refresh_from_db()
        self.assertEqual(self.meetup.title, "Обнавлённый митап")
        self.assertEqual(self.meetup.description, "Новое описание")