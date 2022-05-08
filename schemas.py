from pydantic import BaseModel
from datetime import date


class QuestionsSchema(BaseModel):
    questions_num: int


class QuestionnaireSchema(BaseModel):
    question: str
    answer: str
    date: date


class QuestionnaireCreateSchema(QuestionnaireSchema):
    id: int

    class Config:
        orm_mode = True

