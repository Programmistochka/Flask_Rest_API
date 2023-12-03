from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advertisement
from sqlalchemy.exc import IntegrityError  # ошибка в случае нарушения уник-ти

app = Flask("app")


# зарегистрирован класс ошибок
class HttpError(Exception):
    # определение правильных значений
    def __init__(self, status_code: int, error_message: dict | list | str):
        self.status_code = status_code
        self.error_message = error_message


def get_adv(session: Session, adv_id: int):
    adv = session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, 'advertisement is not found')
    return adv


class AdvsView(MethodView):
    def get(self, adv_id: int):
        with Session() as session:
            adv = get_adv(session, adv_id)
            return jsonify(
                {
                    'id': adv_id,
                    'name': adv.name,
                    'description':adv.description,
                    'creaton_time': adv.creation_time.isoformat(),
                    'author': adv.author
                }
            )

    def post(self):
        json_data = request.json
        
        #print(f'json_data {json_data}')

        with Session() as session:
            adv = Advertisement(**json_data)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'advertisement is already exist')
            return jsonify({'status': 'success', 'id': adv.id})

    def delete(self, adv_id):
        with Session() as session:
            adv = get_adv(session, adv_id)
            session.delete(adv)
            session.commit()
            return jsonify({"status": "success", "id": adv_id})


adv_view = AdvsView.as_view("advertisements")

app.add_url_rule(
    "/advertisements/<int:adv_id>", view_func=adv_view, methods=["GET", "DELETE"]
)
app.add_url_rule("/advertisements/", view_func=adv_view, methods=["POST"])
if __name__ == "__main__":
    app.run()
