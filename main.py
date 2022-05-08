from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import QuestionnaireModel
from core.db import engine
import requests

from schemas import QuestionsSchema

app = FastAPI()


def get_data(session: Session, count: int):
    request = f'https://jservice.io/api/random?count={count}'
    response = requests.get(request).json()

    out = []

    for el in response:
        # create an instance of the database model
        tododb = QuestionnaireModel(
            question=el['question'],
            answer=el['answer'],
            date=el['created_at'])

        # add it to the session and commit it
        if len(tododb.question) != 0:
            session.add(tododb)
            try:
                session.commit()
                out.append(tododb)
                count -= 1
            except IntegrityError:
                session.rollback()

    return {"count": count, "out": out}


@app.post('/api/question')
def get_question(item: QuestionsSchema):
    request = f'https://jservice.io/api/random?count={item.questions_num}'
    response = requests.get(request).json()

    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    out = get_data(session, item.questions_num)

    while out['count'] > 0:
        out = get_data(session, out['count'])

    # close the session
    session.close()
    queryset = (session.query(QuestionnaireModel).all())

    max_id = 0
    for el in queryset:
        if el.id > max_id:
            max_id = el.id

    penultimate_entry = max_id - 1
    rez = session.query(QuestionnaireModel).filter_by(id=penultimate_entry).one_or_none()
    if rez is None:
        return []
    else:
        return rez
