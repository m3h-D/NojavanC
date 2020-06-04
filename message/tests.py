from django.test import TestCase

# Create your tests here.

def add(num1, num2):
    return num1 + num2


class TestOP(TestCase):
    def test_add(self):
        self.assertEqual(add(3,5), 8)