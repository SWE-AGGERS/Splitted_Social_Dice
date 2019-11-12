from flask import jsonify

from reactions_service.app import create_app
from reactions_service.database import db, Reaction
from reactions_service.views.reactions import add_reaction

import unittest
import mock


_app = None


class TestReactionDB(unittest.TestCase):

    def test0(self):
        global _app
        if _app is None:
            tested_app = create_app(debug=True)
            _app = tested_app
        # db.drop_all()
        # db.create_all()
        # create reaction
        with mock.patch('reactions_service.views.reactions.exist_story') as exist_story_mock:
            exist_story_mock.return_value = True
            res = add_reaction(1, 1, 1)
            print(res)




    #
    #
    # def test1(self):
    #     global _app
    #     tested_app = create_app(debug=True)
    #     _app = tested_app
    #
    #     with tested_app.test_client() as client:
    #         init_db_testing(client)
    #         # create like to story 1 from user 1
    #         reply = client.post('/stories/reaction/1/1/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '1')
    #         self.assertEqual(body['reply'], 'Reaction created!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # remove like
    #         reply = client.post('/stories/reaction/1/1/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '1')
    #         self.assertEqual(body['reply'], 'Reaction removed!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # create dislike
    #         reply = client.post('/stories/reaction/1/2/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '2')
    #         self.assertEqual(body['reply'], 'Reaction created!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # change reaction dislike -> like
    #         reply = client.post('/stories/reaction/1/1/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '1')
    #         self.assertEqual(body['reply'], 'Reaction changed!')
    #         self.assertEqual(body['story_id'], '1')
    #
    #         # create dislike
    #         reply = client.post('/stories/reaction/2/2/1')
    #         body = json.loads(str(reply.data, 'utf8'))
    #         self.assertEqual(body['reaction'], '2')
    #         self.assertEqual(body['reply'], 'Reaction created!')
    #         self.assertEqual(body['story_id'], '2')
    #
    #         #
    #         #
    #         # self.assertEqual(body, "{'reaction': '1', 'reply': 'Reaction removed!', 'story_id': '1'}")
    #
    # def test2(self):
    #     global _app
    #     tested_app = create_app(debug=True)
    #     _app = tested_app
    #
    #     with tested_app.test_client() as client:
    #         init_db_testing(client)
    #
    #         for ii in range(1, 101):
    #             # create like to story 1 from user 1
    #             reply = client.post('/stories/reaction/1/1/' + str(ii))
    #             body = json.loads(str(reply.data, 'utf8'))
    #             self.assertEqual(body['reaction'], '1')
    #             self.assertEqual(body['reply'], 'Reaction created!')
    #             self.assertEqual(body['story_id'], '1')
    #
    #         for ii in range(101, 201):
    #             # create like to story 1 from user 1
    #             reply = client.post('/stories/reaction/1/2/' + str(ii))
    #             body = json.loads(str(reply.data, 'utf8'))
    #             self.assertEqual(body['reaction'], '2')
    #             self.assertEqual(body['reply'], 'Reaction created!')
    #             self.assertEqual(body['story_id'], '1')
    #
    #         # get number of like (100)
    #         # get number of dislike (100)

def init_db_testing(client):
    with client.session_transaction() as sess:
        db.drop_all()
        db.create_all()
        #
        # # create 3 likes to story 1
        # like = Reaction()
        # like.story_id = 1
        # like.user_id = 1
        # like.type = 1
        # db.session.add(like)
        # db.session.commit()
        #
        # like = Reaction()
        # like.story_id = 1
        # like.user_id = 2
        # like.type = 1
        # db.session.add(like)
        # db.session.commit()
        #
        # like = Reaction()
        # like.story_id = 1
        # like.user_id = 3
        # like.type = 1
        # db.session.add(like)
        # db.session.commit()

        #
        # like_j = like.to_json()
        # like_j = jsonify(like_j)
