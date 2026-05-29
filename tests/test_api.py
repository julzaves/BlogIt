import unittest
from blogit import create_test_app, db
from blogit.models import Post, Comment


class CommentsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_test_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.user_id = 3
            post = Post(title='Sample Post', content='Sample content.', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()
            self.post_id = post.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# Positive Test Cases
    def test_list_comments_empty(self):
        response = self.client.get(f'/api/posts/{self.post_id}/comments')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_create_comment_success(self):
        response = self.client.post(
            f'/api/posts/{self.post_id}/comments',
            json={'content': 'Nice post!'},
        )
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['content'], 'Nice post!')
        self.assertEqual(data['post_id'], self.post_id)
        self.assertEqual(data['user_id'], 3)

    def test_get_comment_success(self):
        with self.app.app_context():
            comment = Comment(content='Hello', user_id=self.user_id, post_id=self.post_id)
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id

        response = self.client.get(f'/api/comments/{comment_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['id'], comment_id)

    def test_update_comment_success(self):
        with self.app.app_context():
            comment = Comment(content='Old', user_id=self.user_id, post_id=self.post_id)
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id

        response = self.client.put(f'/api/comments/{comment_id}', json={'content': 'Updated'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['content'], 'Updated')

    def test_delete_comment_success(self):
        with self.app.app_context():
            comment = Comment(content='Trash', user_id=self.user_id, post_id=self.post_id)
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id

        response = self.client.delete(f'/api/comments/{comment_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Comment deleted successfully')

        response = self.client.get(f'/api/comments/{comment_id}')
        self.assertEqual(response.status_code, 404)

# Negative/Error Test Cases
    def test_create_comment_missing_content(self):
        response = self.client.post(f'/api/posts/{self.post_id}/comments', json={'user_id': self.user_id})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_create_comment_invalid_post(self):
        response = self.client.post('/api/posts/99999/comments', json={'content': 'Hi', 'user_id': self.user_id})
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_get_comment_not_found(self):
        response = self.client.get('/api/comments/99999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    def test_update_comment_missing_content(self):
        with self.app.app_context():
            comment = Comment(content='Old', user_id=self.user_id, post_id=self.post_id)
            db.session.add(comment)
            db.session.commit()
            comment_id = comment.id

        response = self.client.put(f'/api/comments/{comment_id}', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    def test_delete_comment_not_found(self):
        response = self.client.delete('/api/comments/88888')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

# OpenAPI
    def test_openapi_documentation(self):
        response = self.client.get('/api/openapi.json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['openapi'], '3.0.3')
        self.assertIn('/api/posts/{post_id}/comments', response.get_json()['paths'])
