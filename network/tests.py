import json
from django.test import TestCase, Client
from .models import User, Post


# Create your tests here.
class NetworkTestCase(TestCase):
    def setUp(self):

        # Create users
        u1 = User.objects.create(username="Jim")
        u1.set_password("apple")
        u1.save()
        u2 = User.objects.create(username="Harry", password="new")
        u3 = User.objects.create(username="Han")

        u1.followers.add(u3)

        # Set up Client
        self.client = Client()
        self.client.login(username="Jim", password="apple")

        # Posts
        p1 = Post.objects.create(user=u1, text="One")
        p2 = Post.objects.create(user=u2, text="Two")

    def testPostCount(self):
        self.assertEqual(Post.objects.count(), 2)
    
    def testPostCheckTrue(self):
        u2 = User.objects.get(pk=2)
        p1 = Post.objects.get(user=u2)
        self.assertTrue(p1.isValid())
    
    def test_index(self):
        c = self.client
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["pages_num"], 1)

    def test_posts_index(self):
        c = self.client
        response = c.get("/posts/1")
        self.assertEqual(response.status_code, 201)

    def test_posts_user_201(self):
        c = self.client
        response = c.get("/posts/1?name=Jim")
        self.assertEqual(response.status_code, 201)

    def test_posts_user_404(self):
        c = self.client
        response = c.get("/posts/2?name=Jim")
        self.assertEqual(response.status_code, 404)

    def test_edit_201(self):
        u1 = User.objects.get(pk=1)
        post = Post.objects.get(user=u1)
        c = self.client
        response = c.put("/edit", json.dumps({"text": "apple", "id": post.id}), content_type='application/json')
        post.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(post.text, "apple")

    def test_edit_403(self):
        u2 = User.objects.get(pk=2)
        post = Post.objects.get(user=u2)
        c = self.client
        response = c.put("/edit", json.dumps({"text": "apple", "id": post.id}), content_type='application/json')
        post.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(post.text, "apple")

    def test_like(self):
        u2 = User.objects.get(pk=2)
        post = Post.objects.get(user=u2)
        c = self.client
        response = c.put(f"/like/{post.id}", json.dumps({"like": True}), content_type='application/json')
        self.assertEqual(post.likers.count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_user(self):
        u1 = User.objects.get(pk=1)
        c = self.client
        response = c.get(f"/user?name={u1.username}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profiled_user"], u1)
        self.assertFalse(response.context["is_followed"])
        self.assertEqual(response.context["followers"], 1)
        self.assertEqual(response.context["followed"], 0)
        self.assertEqual(response.context["pages_num"], 1)

    def test_following_posts_201(self):
        c = self.client
        response = c.get("/fposts/1")
        self.assertEqual(response.status_code, 201)
    
    def test_following_posts_404(self):
        c = self.client
        response = c.get("/fposts/2")
        self.assertEqual(response.status_code, 404)

    def test_following(self):
        c = self.client
        response = c.get("/following")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["is_following"])
        self.assertEqual(response.context["pages_num"], 1)