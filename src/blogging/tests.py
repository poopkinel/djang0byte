from django.test import TestCase
from django.db.models import User
from tools.exceptions import (
    AlreadyRatedError, IvalidRateSignError,
    RateDisabledError,
)
from blogging.models import Blog


class BloggingTest(TestCase):
    def setUp(self):
        self.root = User.objects.create(
            username='root',
            is_staff=True,
            is_superuser=True,
        )

    def test_rating(self):
        blog = Blog.objects.create(
            name='blog', description='description',
            author=self.root, is_rate_enabled=False,
        )
        self.assertEqual(blog.is_rated(self.root), False)
        with self.assertRaises(IvalidRateSignError):
            blog.set_rate(-15, self.root)
        blog.set_rate(+1, self.root)
        self.assertEqual(blog.is_rated(self.root), True)
        with self.assertRaises(AlreadyRatedError):
            blog.set_rate(-1, self.root)
        blog2 = Blog.objects.create(
            name='blog', description='description',
            author=self.root,
        )
        with self.assertRaises(RateDisabledError):
            blog2.set_rate(-1, self.root)
