# from django.test import TestCase
# from .models import Rate
# from django.contrib.auth import get_user_model
# from post.models import Post

# User = get_user_model()
# # Create your tests here.
# class RateTestCase(TestCase):
#     # def setUp(self):
#     #     Animal.objects.create(name="lion", sound="roar")
#     #     Animal.objects.create(name="cat", sound="meow")

#     # def test_can_rate(self):
#     @classmethod
#     def setUpTestData(cls):
#         # Create 13 authors for pagination tests
#         # for user_id in range(1, 5):
#         #     print(user_id)
#         Rate.objects.create(
#             user=User.objects.get(id=3),
#             post=Post.objects.get(pk=1),
#             rating=5,
#         )

#     def test_view_url_exists_at_desired_location(self):
#         response = self.client.get('/rate/')
#         self.assertEqual(response.status_code, 200)
