from flask import Blueprint, request, redirect, render_template, abort, json, jsonify
from sqlalchemy import func

from reactions_service.background import update_reactions
from flask import Blueprint, request
from reactions_service.database import db, Reaction

reactions = Blueprint('reactions', __name__)


@reactions.route('/stories/reaction/<storyid>/<reactiontype>', methods=['GET', 'POST'])
def _reaction(storyid, reactiontype):
    try:
        message = add_reaction(reacterid=current_user.id,
                               storyid=storyid, reactiontype=reactiontype)
        # return _stories(error=False, res_msg=message, info_bar=True)
        return jsonify({'reply': message, 'reaction': reactiontype, 'story_id': storyid})
    except StoryNonExistsError as err_msg:
        return _stories(error=True, res_msg=err_msg, info_bar=True)


def add_reaction(reacterid, storyid, reactiontype):
    # TODO call Story service
    q = Story.query.filter_by(id=storyid).first()
    if q is None:
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
    res = update_reactions.delay(story_id=storyid)
    return message


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