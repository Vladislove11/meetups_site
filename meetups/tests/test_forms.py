from django.test import TestCase
from django.contrib.auth.models import User
from ..forms import RegistrationForm, SignUpForm, MeetupForm
from ..models import Location


class RegisttrationFormTest(TestCase):
    def test_valid_email(self):
        form = RegistrationForm(data={"email": "test@example.com"})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = RegistrationForm(data={"email": "not-an-email"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_empty_email(self):
        form= RegistrationForm(data={"email": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_label_in_russian(self):
        form = RegistrationForm()
        self.assertEqual(form.fields["email"].label, "Ваш Email")

class SignUpFormTest(TestCase):
    def test_valid_data(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertTrue(form.is_valid())

    def test_password_dont_match(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "strongpassword123",
            "password2": "differentpassword",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_password_too_short(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "123",
            "password2": "123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_username_already_exists(self):
        User.objects.create_user(username="existing", password="test123")
        form = SignUpForm(data={
            "username": "existing",
            "email": "new@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_email_required(self):
        form = SignUpForm(data={
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_label_in_russian(self):
        form = SignUpForm()
        self.assertEqual(form.fields["username"].label, "Имя пользователя")
        self.assertEqual(form.fields["email"].label, "Email")
        self.assertEqual(form.fields["password1"].label, "Пароль")
        self.assertEqual(form.fields["password2"].label, "Подтверждение пароля")

    def test_save_user(self):
        form = SignUpForm(data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.email, "new@example.com")
        self.assertTrue(user.check_password("strongpassword123"))

class MeetupFormTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(name="Москва", address="Красная площадь, 1")

    def test_valid_data(self):
        form = MeetupForm(data={
            "title": "Новый митап",
            "slug": "new-meetup",
            "description": "Описание",
            "location": self.location.id,
            "organizer_email": "org@example.com"
        })
        self.assertTrue(form.is_valid())

    def test_title_required(self):
        form = MeetupForm(data={
            "slug": "new-meetup",
            "description": "Описание",
            "location": self.location.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_slug_tequired(self):
        form = MeetupForm(data={
            "title": "Новый митап",
            "description": "Описание",
            "location": self.location.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("slug", form.errors)

    def test_description_tequired(self):
        form = MeetupForm(data={
            "title": "Новый митап",
            "slug": "new-meetup",
            "location": self.location.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_labels_in_russian(self):
        form = MeetupForm()
        self.assertEqual(form.fields["title"].label, "Название")
        self.assertEqual(form.fields["description"].label, "Описание")
        self.assertEqual(form.fields["location"].label, "Место")
