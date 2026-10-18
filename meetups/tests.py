from django.test import TestCase

# Create your tests here.
class FirstTest(TestCase):
    def test_math_works(self):
        self.assertEqual(1+1,3)

    def test_string_concatenation(self):
        self.assertEqual("Hello" + " " + "World", "Hello World")