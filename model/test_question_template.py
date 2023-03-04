from model import question_template
from model.question_classify_model import QuestionClassify



def test_get_answer(question):
    # question = "玉米缺钾肥的症状是什么？"
    question_classify = QuestionClassify()
    result = question_classify.predict(question)
    # print(result)

    question_t = question_template.QuestionTemplate()
    answer, cql1, cql2, cql3 = question_t.get_question_answer(question,result)
    lm = "['"
    rm = "']"
    print('答案：' + answer.strip(lm).strip(rm))
    try:
        entity2 = question_t.get_2name()
        entity1 = question_t.get_1name('nr')

    except:
        entity2 = None
        entity1 = None

    return answer.strip(lm).strip(rm),entity1,entity2,cql1,cql2,cql3

#
# if __name__ =="__main__":
#     test_get_answer("")

