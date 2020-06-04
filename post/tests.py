from django.test import TestCase
from django.contrib.auth import get_user_model
from post.models import Post, Category

User = get_user_model()
# Create your tests here.

class CategoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
            for user_id in range(1, 5):
                print(user_id)
                Category.objects.create(
                    title=f'cat {user_id}',
                    # slug=f'Slug {user_id}',
                    description='ok',
                )

class PostTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        for user_id in range(1, 5):
            print(user_id)
            Post.objects.create(
                Author=User.objects.get(id=user_id),
                title=f'Post {user_id}',
                # slug=f'Slug {user_id}',
                content='ok',
                status='published'
            )
            try:
                category.add(Category.objects.get(id=user_id))
            except:
                pass



    # def test_view_url_exists_at_desired_location(self):
    #     response = self.client.get('/rate/')
    #     self.assertEqual(response.status_code, 200)