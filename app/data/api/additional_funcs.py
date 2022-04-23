from flask_restful import abort
from ..db_session import create_session


def abort_if_item_not_found(item_id, item_class):
    session = create_session()
    news = session.query(item_class).get(item_id)
    if not news:
        abort(404, message=f"{item_class.__name__} {item_id} not found")
