from model.question_classify_model import QuestionClassify


def test_question_classify():
    question = "施可丰简介？"
    question_classify = QuestionClassify()
    result = question_classify.predict(question)
    print(result)
    print(f"{question}的分类是：{result}")


if __name__ =="__main__":
    test_question_classify()


