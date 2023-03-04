#  问答类  接受自然问句，构造查询语句，输出答案

from model import question_classify_model
from model import question_template

class QuestionService:
    def __init__(self):
        self.classify_model = question_classify_model.QuestionClassify()
        self.question_template = question_template.QuestionTemplate()

    def get_answer(self,question):
        # 通过分类器获取分类
        question_category = self.classify_model.predict(question)
        try:
            answer = self.question_template.get_question_answer(question,question_category)
        except BaseException as e:
            answer = "我也不知道呢！"

        return answer

question_service_instance = QuestionService()
