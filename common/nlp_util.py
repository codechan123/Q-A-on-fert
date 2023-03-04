import re
import jieba
import jieba.posseg
from common import constant


# 通用的词性标注
def posseg(text):
    jieba.load_userdict(constant.DATA_DIR + "/userdict3.txt")
    clean_text = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、@#￥%&*()]+", "", text)
    result = []
    question_word, question_flag = [], []

    text_cut = jieba.posseg.cut(clean_text)
    return text_cut


# 针对肥料相关的词性标注

def question_posseg(question):
    jieba.load_userdict(constant.DATA_DIR + "/userdict3.txt")
    clean_question = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、@#￥%&*()]+", "",question)
    question_seged = jieba.posseg.cut(str(clean_question))
    result = []
    question_word,question_flag = [], []
    for w in question_seged:
        temp_word = f"{w.word}/{w.flag}"
        result.append(temp_word)

        word,flag = w.word, w.flag
        question_word.append(str(word).strip())
        question_flag.append(str(flag).strip())
    assert len(question_flag) == len(question_word)
    return result