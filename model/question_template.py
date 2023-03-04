import re

from common import nlp_util
from common.neo4j_util import Neo4jQuery

class QuestionTemplate:
    def __init__(self):
        self.q_template_dict = {
            0:self.get_zz,
            1:self.get_fzff,
            2:self.get_flcp,
            3:self.get_syff,
            4:self.get_jj
        }

        self.neo4j_conn = Neo4jQuery()

    def get_question_answer(self,question,template_id):
        question = nlp_util.question_posseg(question)
        question_word,question_flag = [],[]
        print(question)
        for one in question:
            #{item.word}/{item.flag} ,jieba分词后的结果
            word, flag = one.split("/")
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag) == len(question_word)
        self.question_word = question_word
        self.question_flag = question_flag
        self.raw_question = question
        #从dict中获取答案
        try:
            answer, cql1, cql2,cql3 = self.q_template_dict[template_id]()
        except:
            answer = "抱歉，我也不知道这个答案！"
            cql1 = None
            cql2 = None
            cql3 = None
        return answer,cql1,cql2,cql3

    # 获取entity2的名字
    def get_2name(self):
        tag_index = self.question_flag.index("nm")
        movie_name = self.question_word[tag_index]
        return movie_name
    # 获取entity1的名字
    def get_1name(self,type_str):
        name_count = self.question_flag.count(type_str)
        if name_count == 1:
            tag_index = self.question_flag.index(type_str)
            name = self.question_word[tag_index]
            return name
        else:
            result_list = []
            for i,flag in enumerate(self.question_flag):
                if flag == str(type_str):
                    result_list.append(self.question_word[i])
            return result_list

    # 获取数字
    def get_num_x(self):
        x = re.sub(r'\D',"","".join(self.question_word))
        return x
    # MATCH (n:entity1)-[r:jiqi] -> (m:entity2)  WHERE n.name = '施可丰' AND m.name = '施肥机'  RETURN m.syff

    # 获取缺素症状
    def get_zz(self):
        mname = self.get_2name()
        rname = self.get_1name('nr')
        print(rname)
        cql = f"MATCH (n:entity1)-[r:quesu] -> (m:entity2)  WHERE n.name = '{rname}' AND m.name = '{mname}'  RETURN m.zz"
        cql1 = "缺素症"
        cql2 = "症状"
        cql3 = "外在症状"
        print(cql)
        answer = self.neo4j_conn.run(cql)[0:]
        final_answer = str(answer)
        final_cql1 = str(cql1)
        final_cql2 = str(cql2)
        final_cql3 = str(cql3)
        return final_answer,final_cql1,final_cql2,final_cql3

    # 获取缺素治疗方法
    def get_fzff(self):
        mname = self.get_2name()
        rname = self.get_1name('nr')
        cql = f"MATCH (n:entity1)-[r:quesu] -> (m:entity2)  WHERE n.name = '{rname}' AND m.name = '{mname}'  RETURN m.ff"
        cql1 = "缺素症"
        cql2 = "方法"
        cql3 = "推荐方法"
        print(cql)
        answer = self.neo4j_conn.run(cql)[0:]
        final_answer = str(answer)
        final_cql1 = str(cql1)
        final_cql2 = str(cql2)
        final_cql3 = str(cql3)
        return final_answer,final_cql1,final_cql2,final_cql3

    # 获取施可丰的简介
    def get_jj(self):
        rname = self.get_1name('nr')
        print(rname)
        cql = f"MATCH (n) WHERE n.name STARTS WITH '{rname}'  RETURN n.jj"
        print(cql)
        answer = self.neo4j_conn.run(cql)[0:]
        final_answer = str(answer)
        return final_answer

    # 获取机器使用方法
    def get_syff(self):
        mname = self.get_2name()
        # rname = self.get_1name('nr')
        cql = f"MATCH (n:entity1)-[r:jiqi] -> (m:entity2)  WHERE n.name = '施可丰' AND m.name = '{mname}'  RETURN m.syff"
        print(cql)
        cql1 = "设备"
        cql2 = "方法"
        cql3 = "操作"
        answer = self.neo4j_conn.run(cql)[0:]
        final_answer = str(answer)
        final_cql1 = str(cql1)
        final_cql2 = str(cql2)
        final_cql3 = str(cql3)
        return final_answer,final_cql1,final_cql2,final_cql3
    # 获取施可丰肥料
    def get_flcp(self):
        mname = self.get_2name()
        rname = self.get_1name('nr')
        cql = f"MATCH (n:entity1)-[r:chanpin] -> (m:entity2)  WHERE n.name = '{rname}' AND m.name = '{mname}'  RETURN m.cp"
        # cql1 = f"MATCH (n:entity1)-[r] -> (m:entity2)  WHERE n.name = '{rname}' AND m.name = '{mname}' RETURN type(r) as type"
        cql1 = "产品"
        cql2 = "介绍"
        cql3 = "系列"
        print(cql)
        print(cql1)
        answer = self.neo4j_conn.run(cql)[0:]

        final_answer = str(answer)
        final_cql1 = str(cql1)
        final_cql2 = str(cql2)
        final_cql3 = str(cql3)
        return final_answer,final_cql1,final_cql2,final_cql3