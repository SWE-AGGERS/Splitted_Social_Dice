
from flask import jsonify
from reactions_service.background import count_reactions_async
from flask import Blueprint
from reactions_service.database import db, Reaction, Counters

reacts = Blueprint('reacts', __name__)


@reacts.route('/stories/reaction/<storyid>/<reactiontype>/<reacterid>', methods=['POST'])
def _reaction(storyid, reactiontype, reacterid):
    try:
        resp_json = add_reaction(reacterid=reacterid, storyid=storyid, reactiontype=reactiontype)
        return resp_json
    except StoryNonExistsError as err_msg:
        return jsonify({'reply': 'Error', 'reaction': reactiontype, 'story_id': storyid})


@reacts.route('/stories/reaction_count/<storyid>', methods=['GET'])
def _reactions(storyid, reactiontype):
    # return number of like and dislike for a story (async updated)
    try:
        message = count_reaction(storyid=storyid)
        return jsonify({'reply': message, 'reaction': reactiontype, 'story_id': storyid})
    except StoryNonExistsError as err_msg:
        return jsonify({'reply': 'error', 'reaction': reactiontype, 'story_id': storyid})


def exist_story():
    return False


def add_reaction(reacterid, storyid, reactiontype):
    # TODO call Story service
    # q = Story.query.filter_by(id=storyid).first()
    # if q is None:
    #     raise StoryNonExistsError('Story not exists!')

    res = exist_story()
    if not res:
        raise StoryNonExistsError('Story not exists!')

    old_reaction = Reaction.query.filter_by(
        user_id=reacterid, story_id=storyid).first()

    if old_reaction is None:
        new_reaction = Reaction()
        new_reaction.user_id = reacterid
        new_reaction.story_id = storyid
        new_reaction.type = reactiontype
        db.session.add(new_reaction)
        db.session.commit()
        message = 'Reaction created!'

    else:
        if int(reactiontype) == int(old_reaction.type):
            message = 'Reaction removed!'
            db.session.delete(old_reaction)
            db.session.commit()
        else:
            old_reaction.type = reactiontype
            db.session.commit()
            message = 'Reaction changed!'
        # # Update DB counters
    res = count_reactions_async.delay(story_id=storyid)
    return jsonify({'reply': message, 'reaction': reactiontype, 'story_id': storyid})


class StoryNonExistsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def reacted(user_id, story_id):
    q = db.session.query(Reaction).filter_by(
        story_id=story_id, user_id=user_id).all()

    if len(q) > 0:
        return q[0].type
    return 0


def count_reaction(storyid):
    q = Counters.query.filter_by(story_d=storyid).first()
    return q.to_json()

