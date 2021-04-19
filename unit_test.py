from Facebooker import facebook
from test_constant import *
import unittest


class FBUnitTest(unittest.TestCase):
    fb = facebook.API()

    def __init__(self, *args):
        self.fb.login(EMAIL,
                      PASSWORD)
        super().__init__(*args)

    def test_login(self):
        self.assertTrue(self.fb.login_check)

    def test_get_user_post_list(self):
        post_generator = self.fb.get_user_post_list(TEST_USER_ID)
        post_id = next(post_generator)
        self.assertIsNotNone(post_id)

    def test_get_post(self):
        post_info = self.fb.get_post(TEST_POST_ID)
        self.assertEqual(post_info.id, TEST_POST_ID)
        self.assertEqual(post_info.author, TEST_POST_AUTHOR)
        self.assertEqual(post_info.content, TEST_POST_CONTENT)

    def test_get_comments(self):
        comment = self.fb.get_comments(TEST_POST_ID)[-1]
        self.assertIn(comment.id, TEST_COMMNENT_ID)
        self.assertEqual(comment.content, TEST_COMMENT_CONTENT)

    def test_get_replies(self):
        reply = self.fb.get_replies(TEST_POST_ID, TEST_COMMNENT_ID)[-1]
        self.assertEqual(reply.id, TEST_REPLY_ID)
        self.assertEqual(reply.content, TEST_REPLY_CONTENT)


if __name__ == '__main__':
    unittest.main()
