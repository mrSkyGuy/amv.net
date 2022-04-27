from flask_restful import abort
from ..db_session import create_session


def abort_if_item_not_found(item_id, item_class):
    """ 404, если элемент не был найден """
    session = create_session()
    item = session.query(item_class).get(item_id)
    if not item:
        abort(404, success=False, message=f"{item_class.__name__} {item_id} not found")
