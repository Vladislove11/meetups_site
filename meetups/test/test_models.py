from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Meetup, Location, Participant


# Create your tests here.
# class FirstTest(TestCase):
#     def test_math_works(self):
#         self.assertEqual(1+1,2)

#     def test_string_concatenation(self):
#         self.assertEqual("Hello" + " " + "World", "Hello World")

class LoocationModelTest(TestCase):
    def test_str(self):
        location = Location.objects.create(
            name = "Москва",
            address = "Красная площадь, 1"
        )
        self.assertEqual(str(location), "Москва (Красная площадь, 1)")

    def test_fields(self):
        location = Location.objects.create(
            name = "Санкт-Петербург",
            address = "Невский проспект, 1"
        )
        self.assertEqual(location.name, "Санкт-Петербург")
        self.assertEqual(location.address, "Невский проспект, 1")

class ParticipantModelTest(TestCase):
    def test_str(self):
        participant = Participant.objects.create(email="test@example.com")
        self.assertEqual(str(participant), "test@example.com")

    def test_email_unique(self):
        Participant.objects.create(email="test@example.com")
        with self.assertRaises(Exception):
            Participant.objects.create(email="test@example.com")

    def test_user_optional(self):
        participant = Participant.objects.create(email="nouser@example.com")
        self.assertIsNone(participant.user)


class MeetupModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            name="Москва",
            address="Красная площадь, 1"
        )
        self.meetup = Meetup.objects.create(
            title = "Тестовый митап",
            slug = "test-meetup",
            description = "Описание тестового митапа",
            location = self.location
        )

    def test_str(self):
        # self.meetup уже создан в setup
        self.assertEqual(str(self.meetup), "Тестовый митап (test-meetup)")

    def test_fields(self):
        self.assertEqual(self.meetup.title, "Тестовый митап")
        self.assertEqual(self.meetup.slug, "test-meetup")
        self.assertEqual(self.meetup.description, "Описание тестового митапа")

    def test_location_relation(self):
        self.assertEqual(self.meetup.location, self.location)
        self.assertEqual(self.meetup.location.name, "Москва")

    def test_slug_unique(self):
        with self.assertRaises(Exception):
            Meetup.objects.create(
                title="Другой митап",
                slug="test-meetup",
                description="Описание"
            )

    def test_participants_empty_by_default(self):
        self.assertEqual(self.meetup.participants.count(), 0)

    def test_add_participant(self):
        participant = Participant.objects.create(email="user@example.com")
        self.meetup.participants.add(participant)
        self.assertEqual(self.meetup.participants.count(), 1)
        self.assertIn(participant, self.meetup.participants.all())

    def test_creator_optional(self):
        self.assertIsNone(self.meetup.creator)

    def test_creator_relation(self):
        user = User.objects.create_user(username="testuser", password="test123")
        self.meetup.creator = user
        self.meetup.save()
        self.assertEqual(self.meetup.creator, user)
        self.assertEqual(self.meetup.creator.username, "testuser")