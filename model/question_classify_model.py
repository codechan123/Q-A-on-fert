import os
import re
import jieba
from common import file_util, constant
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from common import nlp_util

class QuestionClassify:
    def __init__(self):
        self.train_x,self.train_y = load_train_data()
        # 文本向量化
        self.tfidf_vec = TfidfVectorizer()
        self.train_vec = self.tfidf_vec.fit_transform(self.train_x).toarray()
        self.model = self.train_model_nb()

# 训练模型
    def train_model_nb(self):
        nb =MultinomialNB(alpha=0.01)
        nb.fit(self.train_vec,self.train_y)
        return nb

#预测分类
    def predict(self,question):
        text_cut_gen = nlp_util.posseg(question)
        # 获取模板
        # 替换nr（实体1） nm（实体2）
        # 原始问题
        text_src_list = []
        # 一般化的问题  flag是词性的标注
        text_normal_list = []
        for item in text_cut_gen:
            text_src_list.append(item.word)
            if item.flag in ['nr', 'nm', 'ng']:
                text_normal_list.append(item.flag)
            else:
                text_normal_list.append(item.word)
        question_normal = [" ".join(text_normal_list)]
        question_vector = self.tfidf_vec.transform(question_normal).toarray()
        predict = self.model.predict(question_vector)[0]
        return predict

# 词性标注
def load_train_data():
    train_x = []
    train_y = []
    file_path_list = file_util.get_file_list(os.path.join(constant.DATA_DIR,"question"))
    for file_item in file_path_list:
        # 获取文件名中的label
        label = re.sub(r'\D', "", file_item)
        if label.isnumeric():
            label_num = int(label)
            # 读取文件的内容
            with(open(file_item,"r",encoding="utf-8")) as file:
                lines = file.readlines()
                for line in lines:
                    word_list = list(jieba.cut(str(line).strip()))
                    # 获取文件中的内容
                    train_x.append(" ".join(word_list))
                    # 获取文件中的标签
                    train_y.append(label_num)
    return train_x, train_y