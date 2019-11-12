from celery import Celery

from reactions_service.database import db, Reaction, Counters
from sqlalchemy import and_

BACKEND = BROKER = 'redis://localhost:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

_APP = None

#
# @celery.task
# def update_reactions(story_id):
#     global _APP
#     if _APP is None:
#         from reactions_service.app import create_app
#         app = create_app()
#         # db.init_app(app)
#     else:
#         app = _APP
#     with app.app_context():
#         # TODO call the Story service
#         q = Story.query.filter_by(id=story_id).first()
#         # count the likes, dislikes
#         # use the first column for efficiency
#         # [https://stackoverflow.com/questions/14754994/why-is-sqlalchemy-count-much-slower-than-the-raw-query]
#         num_likes = db.session.query(Reaction.story_id).filter_by(
#             story_id=story_id, type=1).count()
#         num_dislikes = db.session.query(Reaction.story_id).filter_by(
#             story_id=story_id, type=2).count()
#         # update likes and dislikes counters
#         q.likes = num_likes
#         q.dislikes = num_dislikes
#         db.session.commit()


@celery.task
def count_reactions_async(story_id):
    # story existed (previously queried Story Service)
    global _APP
    if _APP is None:
        from reactions_service.app import create_app
        app = create_app()
    else:
        app = _APP
    with app.app_context():
        q = Counters.query.filter_by(story_id=story_id).first()
        if q is not None:
            num_likes = db.session.query(Reaction.story_id).filter_by(
                story_id=story_id, type=1).count()
            num_dislikes = db.session.query(Reaction.story_id).filter_by(
                story_id=story_id, type=2).count()

            q.likes = num_likes
            q.dislikes = num_dislikes
            db.session.commit()
            return True
        return False
