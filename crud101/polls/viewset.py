from viewflow.urls import ModelViewset

from .models import Question


class QuestionViewset(ModelViewset):
    model = Question
