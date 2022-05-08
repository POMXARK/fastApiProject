from sqlalchemy import Column, Integer, String, DateTime

from core.db import Base


class QuestionnaireModel(Base):
    """alembic revision --autogenerate -m 'Fist' """
    """ alembic upgrade head """
    __tablename__ = "questionnaire"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    question = Column(String, unique=True)
    answer = Column(String(350))
    date = Column(DateTime)
