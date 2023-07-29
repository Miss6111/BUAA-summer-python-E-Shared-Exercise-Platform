# import openpyxl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session  # 数据库操作核心
from sqlalchemy.ext.declarative import declarative_base  # 父类
from sqlalchemy import or_
from datetime import datetime
from sqlalchemy import DateTime

Base = declarative_base()
DB_connect = 'mysql+mysqldb://root:222333dyh@localhost/Test'
engine = create_engine(DB_connect, echo=True)


# 评论表
class Comments(Base):
    __tablename__ = 'comments'
    id = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    sender = sqlalchemy.Column(sqlalchemy.Integer)  # 评论的userid
    qid = sqlalchemy.Column(sqlalchemy.Integer)  # 对哪个问题评论
    content = sqlalchemy.Column(sqlalchemy.String(200))  # 评论内容


# 收藏问题_stu
class Star_stu(Base):
    __tablename__ = 'star_stu'
    uid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("stus.uid"), primary_key=True)
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("questions.qid"), primary_key=True)


# 多对多表
class Chap_ques(Base):  # 存问题-章节
    __tablename__ = 'chap_ques'
    name = sqlalchemy.Column(sqlalchemy.String(20), sqlalchemy.ForeignKey("chapters.name"), primary_key=True)
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("questions.qid"), primary_key=True)


class Ques_qgroup(Base):  # 存每个问题---问题组
    __tablename__ = 'ques_qgroup'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("qgroups.gid"), primary_key=True)
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("questions.qid"), primary_key=True)


class Stu_group(Base):  # 学生--学生小组
    __tablename__ = 'stu_group'
    uid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("stus.uid"), primary_key=True)
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("groups.gid"), primary_key=True)


class Stu_qgroup(Base):  # 学生--问题组
    __tablename__ = 'stu_qgroup'
    uid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("stus.uid"), primary_key=True)
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("qgroups.gid"), primary_key=True)


class Ggroup_group(Base):  # 存问题组--学生组
    __tablename__ = 'qgroup_group'
    qgid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("qgroups.gid"), primary_key=True)
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, sqlalchemy.ForeignKey("groups.gid"), primary_key=True)


class Chapters(Base):  # 有哪些章节
    __tablename__ = 'chapters'
    name = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)
    ques = sqlalchemy.orm.relationship("Questions", secondary="chap_ques", backref="Chapters",
                                       cascade='all')  # 这个章节对应的所有题


class Questions(Base):  # 有哪些问题
    __tablename__ = 'questions'
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)  # 当前问题的编号
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创建人的id
    name = sqlalchemy.Column(sqlalchemy.String(20))  # 题目
    title = sqlalchemy.Column(sqlalchemy.String(1000))  # 题干
    chapter = sqlalchemy.Column(sqlalchemy.String(10))  # 章节
    # 所属问题组
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary="ques_qgroup", backref="Questions", cascade='all')
    # 题型,0选择，1填空
    type = sqlalchemy.Column(sqlalchemy.Integer)
    # ”1010“为选AC
    answer = sqlalchemy.Column(sqlalchemy.String(5))
    # ABCD四个选项，填空默认显示A
    answerA = sqlalchemy.Column(sqlalchemy.String(100))
    answerB = sqlalchemy.Column(sqlalchemy.String(100))
    answerC = sqlalchemy.Column(sqlalchemy.String(100))
    answerD = sqlalchemy.Column(sqlalchemy.String(100))
    # 填空题答案
    gap = sqlalchemy.Column(sqlalchemy.String(20))
    public = sqlalchemy.Column(sqlalchemy.Boolean)  # 是否是所有人可见
    total = sqlalchemy.Column(sqlalchemy.Integer)
    right = sqlalchemy.Column(sqlalchemy.Integer)


class Stus(Base):
    __tablename__ = 'stus'  # 名字
    uid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    # 进行属性与字段映射，名字可以不一
    name = sqlalchemy.Column(sqlalchemy.String(50))

    password = sqlalchemy.Column(sqlalchemy.String(50))
    # 用户组信息
    groups = sqlalchemy.orm.relationship("Groups", secondary="stu_group", backref="Stus", cascade='all')
    # 问题组信息，即那些问题组对当前用户开放
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary="stu_qgroup", backref="Stus", cascade='all')
    # 收藏的问题
    starquestions = sqlalchemy.orm.relationship("Questions", secondary="star_stu", backref="Stus", cascade='all')
    # 格言
    quote = sqlalchemy.Column(sqlalchemy.String(100))
    # 简介
    Bi = sqlalchemy.Column(sqlalchemy.String(100))
    # 是否是管理员
    issuper = sqlalchemy.Column(sqlalchemy.Boolean)


class Groups(Base):  # 用户小组
    __tablename__ = 'groups'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)  # 组id
    name = sqlalchemy.Column(sqlalchemy.String(50))  # 组名
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创造者的id
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary="qgroup_group", backref="Groups")  # 这个用户小组拥有权限的问题小组


class QGroups(Base):  # 问题小组，由每个用户主动创建
    __tablename__ = 'qgroups'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创造者
    name = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)


# 做题记录
class Records(Base):
    __tablename__ = 'records'
    uid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    right = sqlalchemy.Column(sqlalchemy.Boolean, primary_key=True)
    time = sqlalchemy.Column(DateTime, default=datetime.now)
    rate = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)


def create_session():  # session用来操作数据库
    """

    :return:
    """
    session_ = sessionmaker(bind=engine)  # 一个session是一个对数据库链接的包装
    session = session_()  # 实例化session对象
    return session


def check_name(C, name):
    """

    :param C:
    :param name:
    :return:
    """
    session = create_session()
    if len(session.query(C).filter(C.name == name).all()) == 0:
        session.close()
        return True
    session.close()
    return False


# 任务一，个人信息管理
def create_new_user(name, password, manager):  # 按下注册确定按键的瞬间,创建新用户
    """

    :param name:
    :param password:
    :param manager:
    :return:
    """
    s = create_session()
    if not check_name(Stus, name):
        s.close()
        return False
    else:
        new = Stus(name=name, password=password, issuper=manager, Bi="你还没有写任何简介", quote="", groups=[],
                   qgroups=[])
        s.add(new)
        s.commit()
        s.close()
        return True


def change_password(password, name):  # 改密码
    """

    :param password:
    """
    s = create_session()
    s.query(Stus).filter(Stus.name == name).first().password = password
    s.commit()
    s.close()


def change_name(new, name):  # 改名字，按下确定瞬间
    """

    :param new:
    :return:
    """
    if not check_name(Stus, new):
        return False
    else:
        s = create_session()
        stu = s.query(Stus).filter(Stus.name == name).first()
        stu.name = new
        s.commit()
        s.close()
        return True


# 当前用户属于的所有组
def show_users_groups(name):
    s = create_session()
    groups = []
    for i in s.query(Stus).filter(Stus.name == name).first().groups:
        groups.append(i.name)
    s.close()
    return groups


def change_quote(new, name):  # 改格言
    """

    :param new:
    """
    s = create_session()
    s.query(Stus).filter(Stus.name == name).first().quote = new
    s.commit()
    s.close()


def change_bi(new, name):  # 改简介
    """

    :param new:
    """
    s = create_session()
    s.query(Stus).filter(Stus.name == name).first().Bi = new
    s.commit()
    s.close()


def login(name, password):  # 登入瞬间
    """

    :param name:
    :param password:
    :return:
    """
    s = create_session()
    if check_name(Stus, name):  # 没这个账号名
        return False
    else:
        passw = s.query(Stus).filter(Stus.name == name).first().password
        if passw == password:  # 账号密码都正确
            s.close()
            return True
        else:
            s.close()
            return False


# 任务二 管理员创建小组，将他人加入小组，用户搜索加入小组，注意，此时要更新学生的问题组权限
def check_super(name):
    """

    :return:
    """
    s = create_session()
    ans = s.query(Stus).filter(Stus.name == name).first().issuper
    s.close()
    return ans


def all_groups():  # 管理员界面使用，目前的所有用户小组
    groups = []
    s = create_session()
    all = s.query(Groups).all()
    for i in all:
        groups.append(i.name)
    return groups


#
#
#
#
def create_new_group(g_name, name):  # 创建一个空的新的小组(小组名)
    """

    :param g_name:
    :return:
    """
    s = create_session()
    if not check_name(Groups, g_name):  # 名字存在
        s.close()
        return False
    else:
        uid = s.query(Stus).filter(Stus.name == name).first().uid
        new = Groups(name=g_name, uid=uid)
        s.add(new)
        s.commit()
        s.close()


# 将一组人加进group，注意问题权限
def add_into_group(users, g_name):  # 此处users为名字字符串数组
    """

    :param users:
    :param g_name:
    """
    s = create_session()
    g_name = g_name.strip()
    group = s.query(Groups).filter(Groups.name == g_name).first()  # 找到当前学生gruop

    for i in users:  # 遍历每一个学生
        stu = s.query(Stus).filter(Stus.name == i.strip()).first()
        stu.groups.append(group)  # 保证此时学生一定不在这个组

        for j in group.qgroups:  # 当前group的qgroups
            if not j in stu.qgroups:  # 这个学生目前的qgroups中不存在的才加入
                stu.qgroups.append(j)  # 学生加入权限
    s.commit()
    s.close()


def search_for_groups(gname, name):  # 搜索组用，除去了当前用户已经在的组
    s = create_session()
    gname = gname.strip()
    groups = s.query(Groups).filter(Groups.name.like('%' + gname + '%')).all()
    names = []
    uid = s.query(Stus).filter(Stus.name == name).first().uid
    temps = []
    for i in groups:
        inGroups = s.query(Stu_group).filter(Stu_group.uid == uid).all()
        for j in inGroups:
            temps.append(j.gid)
        if not i.gid in temps:
            names.append(i.name)
    return names
    s.close()


def search_students(gname, name):  # 去除了已经在表里的人
    """

    :param gname:
    :param name:
    :return:
    """
    s = create_session()
    gname = gname.strip()
    gid = s.query(Groups).filter(Groups.name == gname).first().gid
    uids_ = s.query(Stu_group).filter(Stu_group.gid == gid).all()
    uids = []
    for i in uids_:
        uids.append(i.uid)
    students = s.query(Stus).filter(Stus.name.like('%' + name + '%')).all()
    unames = []
    for i in students:
        if not i.uid in uids:
            unames.append(i.name)
    # 符合要求所有学生名字
    s.commit()
    s.close()
    return unames


# def delete_from_group(users, gname):  # 将部分人从组里删除
#     """
#
#     :param users:
#     :param gname:
#     """
#     s = create_session()
#     group = s.query(Groups).filter(Groups.name == gname).first()
#     qgroups = group.qgroups
#     for i in users:
#         user = s.query(Stus).filter(Stus.name == i).first()
#         user.groups.remove(group)
#         for j in qgroups:
#             user.groups.remove(j)
#     s.commit()
#     s.close()


def search_groups(page):  # 用户查找组时
    """

    :param page:
    :return:
    """
    # 分页显示，每页十条
    s = create_session()
    groups = s.query(Groups).limit(10).offset((page - 1) * 10).all()
    gnames = []
    for i in groups:
        gnames.append(i.name)
    s.close()
    # 返回值是组名数组
    return gnames


def user_add_into_group(gnames, name):  # 用户主动申请加入一串组,此时保证用户都不在这些组里
    """

    :param name:
    :param gnames:
    :return:
    """
    s = create_session()
    # 如果已经在组里，加入失败
    groups = s.query(Groups).filter(Groups.name.in_(gnames)).all()
    stu = s.query(Stus).filter(Stus.name == name).first()
    for i in groups:
        stu.groups.append(i)  # 关联的是整个而不是一个值
        print(i.name)
    for group in groups:
        qgroups = group.qgroups  # 当前group的qgroups
        # 这个学生目前的qgroups中不存在的才加入
        for j in qgroups:
            print(j.name)
            if not j in stu.qgroups:
                stu.qgroups.append(j)  # 学生加入权限
    s.commit()
    s.close()


# 任务三 上传 单个问题 或 一个文件的问题
def show_all_chapter():  # 返回所有的章节名字
    """

    :return:
    """
    s = create_session()
    name = []
    for i in s.query(Chapters).all():
        name.append(i.name)
    s.close()
    return name


def load_one_question(title, answer, chapter, my_type, answer1, answer2, answer3, answer4, gap, public, creater):
    """


    :param creater:
    :param title:
    :param answer:
    :param chapter:
    :param my_type:
    :param answer1:
    :param answer2:
    :param answer3:
    :param answer4:
    :param public:
    """
    s = create_session()
    c = s.query(Chapters).filter(Chapters.name == chapter).first()
    q = Questions(title=title, answer=answer, type=my_type, answerA=answer1, answerB=answer2, answerC=answer3,
                  answerD=answer4, gap=gap, public=public, uid=s.query(Stus).filter(Stus.name == creater).first().uid,
                  total=0, right=0, chapter=chapter)
    s.add(q)
    s.commit()
    c.ques.append(q)
    s.commit()
    s.close()
    # 分组，给问题加标签


# def load_files(path, name):  # 需要规定文件格式？？再想
#     """
#
#     :param name:
#     :param path:
#     """
#     f = openpyxl.load_workbook(path)
#     names = f.get_sheet_names()  # 所有sheet
#     for sheet_name in names:  # 每一页
#         sheet = f.get_sheet_by_name(sheet_name)
#         rows = sheet.max_row
#         for i in range(rows):  # 每一行是一个问题
#             title = sheet.cell(i + 1, 1).value
#             answer = sheet.cell(i + 1, 2).value
#             chapter = sheet.cell(i + 1, 3).value
#             mytype = sheet.cell(i + 1, 4).value
#             answer1 = sheet.cell(i + 1, 5).value
#             answer2 = sheet.cell(i + 1, 6).value
#             answer3 = sheet.cell(i + 1, 7).value
#             answer4 = sheet.cell(i + 1, 8).value
#             # 默认是公开的
#             load_one_question(title, answer, chapter, mytype, answer1, answer2, answer3, answer4, public=True,
#                               creater=name)


# def select_questions(chapters_name, mytype, user_name):  # 选择哪些chapters,填空,选择,权限
#     """
#
#     :param chapters_name:
#     :param type:
#     :return:
#     """
#     # 自己创造的题+public的题+所属用户小组拥有的题
#     # s = create_session()
#     # q = s.query(Questions).filter(or_(Questions.chapter.in_(chapters_name), Questions.public == True)).filter(
#     #     Questions.type == mytype).all()
#     # groups = s.query(Stus).filter(Stus.name == user_name).first().groups
#     # gids = []  # 用户在的所有组
#     # for i in groups:
#     #     gids.append(i.gid)
#     #
#     # questions = []
#     # for i in q:  # 遍历每个问题
#     #     qgids = []  # 问题属于的问题组
#     #     for j in i.qgroups:
#     #         qgids.append(j.gid)
#     #     if len(s.query(Ggroup_group).filter(Ggroup_group.gid.in_(gids)).filter(
#     #             Ggroup_group.qgid.in_(qgids)).all()) != 0:
#     #         questions.append(i)
#     #
#     # s.close()
#     # # 返回值是所有符合要求的问题
#     # return questions
#     pass


# 根据关键词搜索问题
def scope_questions(ques_name, chapters_name, mytype, user_name):  # 关键词，章节，题型
    """

    :param ques_name:
    :param chapters_name:
    :param mytype:
    :param user_name:
    :return:
    """
    s = create_session()
    # 搜索范围包括questions中的public或上传者为本人的，和qgroup中的
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    qgroups = s.query(Stus).filter(Stus.name == user_name).first().qgroups
    q = s.query(Questions).filter(or_(Questions.uid == uid, Questions.public == True,
                                      Questions.qgroups.in_(qgroups))) \
        .filter(Questions.chapter.in_(chapters_name)).filter(Questions.type == mytype).filter(
        Questions.title.find(ques_name)).all()
    # 目前仅支持关键词为title子串
    s.commit()
    s.close()
    return q  # 返回值为满足要求的Questions条目


# ************************************************************************************************************** #
# 根据关键词搜索问题
def scope_questions_title(ques_name, chapters_name, mytype, user_name):  # 关键词，章节，题型
    """

    :param ques_name:
    :param chapters_name:
    :param mytype:
    :param user_name:
    :return:
    """
    s = create_session()
    # 搜索范围包括questions中的public或上传者为本人的，和qgroup中的
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    qgroups = s.query(Stus).filter(Stus.name == user_name).first().qgroups
    q = s.query(Questions).filter(or_(Questions.uid == uid, Questions.public == True,
                                      Questions.qgroups.in_(qgroups))) \
        .filter(Questions.chapter.in_(chapters_name)).filter(Questions.type == mytype).filter(
        Questions.title.find(ques_name)).all()
    # ************************************** #
    title = []
    for i in q:
        title.append(i.title)
    # ************************************** #
    # 目前仅支持关键词为title子串
    s.commit()
    s.close()
    return title  # 返回值为满足要求的Questions条目


def scope_questions_answer(ques_name, chapters_name, mytype, user_name):  # 关键词，章节，题型
    """

    :param ques_name:
    :param chapters_name:
    :param mytype:
    :param user_name:
    :return:
    """
    s = create_session()
    # 搜索范围包括questions中的public或上传者为本人的，和qgroup中的
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    qgroups = s.query(Stus).filter(Stus.name == user_name).first().qgroups
    q = s.query(Questions).filter(or_(Questions.uid == uid, Questions.public == True,
                                      Questions.qgroups.in_(qgroups))) \
        .filter(Questions.chapter.in_(chapters_name)).filter(Questions.type == mytype).filter(
        Questions.title.find(ques_name)).all()
    # ************************************** #
    answer = []
    for i in q:
        answer.append(i.answer)
    # ************************************** #
    # 目前仅支持关键词为title子串
    s.commit()
    s.close()
    return answer  # 返回值为满足要求的Questions条目


def scope_questions_type(ques_name, chapters_name, mytype, user_name):  # 关键词，章节，题型
    """

    :param ques_name:
    :param chapters_name:
    :param mytype:
    :param user_name:
    :return:
    """
    s = create_session()
    # 搜索范围包括questions中的public或上传者为本人的，和qgroup中的
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    qgroups = s.query(Stus).filter(Stus.name == user_name).first().qgroups
    q = s.query(Questions).filter(or_(Questions.uid == uid, Questions.public == True,
                                      Questions.qgroups.in_(qgroups))) \
        .filter(Questions.chapter.in_(chapters_name)).filter(Questions.type == mytype).filter(
        Questions.title.find(ques_name)).all()
    # ************************************** #
    mytype = []
    for i in q:
        mytype.append(i.type)
    # ************************************** #
    # 目前仅支持关键词为title子串
    s.commit()
    s.close()
    return mytype  # 返回值为满足要求的Questions条目


def scope_questions_qid(ques_name, chapters_name, mytype, user_name):  # 关键词，章节，题型
    """

    :param ques_name:
    :param chapters_name:
    :param mytype:
    :param user_name:
    :return:
    """
    s = create_session()
    # 搜索范围包括questions中的public或上传者为本人的，和qgroup中的
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    qgroups = s.query(Stus).filter(Stus.name == user_name).first().qgroups
    q = s.query(Questions).filter(or_(Questions.uid == uid, Questions.public == True,
                                      Questions.qgroups.in_(qgroups))) \
        .filter(Questions.chapter.in_(chapters_name)).filter(Questions.type == mytype).filter(
        Questions.title.find(ques_name)).all()
    # ************************************** #
    qid = []
    for i in q:
        qid.append(i.qid)
    # ************************************** #
    # 目前仅支持关键词为title子串
    s.commit()
    s.close()
    return qid  # 返回值为满足要求的Questions条目
# ************************************************************************************************************** #


# 问题共享功能
def create_own_ques_group(name, user_name):  # 某个用户可以选择构造一个问题组并命名，类比学生和学生组
    """

    :param name:
    :return:
    """
    if check_name(QGroups, name) == False:
        return False
    s = create_session()
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    new = QGroups(name=name, uid=uid)
    s.add(new)
    s.commit()
    s.close()
    return True


def add_ques_into_group(name, questions):  # 传入问题编号/后续可以考虑改成名字
    """

    :param name:
    :param questions:
    """
    s = create_session()
    group = s.query(QGroups).filter(QGroups.name == name).first()
    for i in questions:  # 将选中问题加入问题组中
        temp = s.query(Questions).filter(Questions.qid == i).first()
        temp.qgroups.append(group)
    s.commit()
    s.close()


def share_question_with_groups(qgname, gname):  # 与特定的用户组分享特定的问题组
    """

    :param qgname:
    :param gname:
    """
    s = create_session()
    gid = s.query(Groups).filter(Groups.name == gname).first().gid  # 得到这个用户组的gid
    temp = s.query(Stu_group).filter(Stu_group.gid == gid).all()  # 得到用户组的所有用户的uid
    ids = []
    for i in temp:
        ids.append(i.uid)
    stus = s.query(Stus).filter(Stus.uid.in_(ids)).all()  # 得到用户组所有用户
    qgroup = s.query(QGroups).filter(QGroups.name == qgname).first()
    s.query(Groups).filter(Groups.name == gname).first().qgroups.append(qgroup)
    for i in stus:
        if qgroup in i.qgroups == False:
            i.qgroups.append(qgroup)  # 依次建立联系
    s.commit()
    s.close()


# 只关心当前评论显示在在哪个答案的下方
def send_comments(qid, content, user_name):
    """

    :param user_name:
    :param qid:
    :param content:
    """
    s = create_session()
    stu = s.query(Stus).filter(Stus.name == user_name).first()
    new = Comments(qid=qid, content=content, sender=stu.uid)  # 保证不能被改变
    s.add(new)
    s.commit()
    s.close()


# 点击加号显示所有的评论-->下画框
def show_some_comments():
    """

    :return: 返回三条评论
    """
    s = create_session()
    re = []
    comments = s.query(Comments).limit(3).all()
    for i in comments:
        sender = s.query(Stus).filter(Stus.uid == i.sender).first().name
        re.append([i.content, sender])
    s.close()
    return re  # 返回的是[内容，发送人]


def show_more_comments():
    """
   # 全部评论
    :return: 返回全部评论
    """
    s = create_session()
    re = []
    comments = s.query(Comments).all()
    for i in comments:
        sender = s.query(Stus).filter(Stus.uid == i.sender).first().name
        re.append([i.content, sender])
    s.close()
    return re  # 返回的是[内容，发送人]


def search_for_sen(word):
    """
:return
    """
    s = create_session()
    all = s.query(Questions).filter(Questions.title.like(word)).all()
    return all


def generate_talent_tabel():
    """
:return
    """
    # 日期和错题记录
    pass


def search_star_questions(page, name):  #
    """

    :param page:
    :return:
    """
    # 分页显示，每页十条
    s = create_session()
    id = s.query(Stus).filter(Stus.name == name).first().uid
    temps = s.query(Star_stu).filter(Star_stu.uid == id).limit(10).offset((page - 1) * 10).all()
    questions = []
    for i in temps:
        questions.append(s.query(Questions).filter(Questions.qid == i.qid).first())
    s.close()
    # 返回值是存有问题的数组
    return questions


def drop_and_create():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('drop and create')


def do_question(qid, user_name, answer, gap):  # 题目id;是否正确
    s = create_session()
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    # 判单正确与否
    mytype = s.query(Questions).filter(Questions.uid == uid).first().type
    myanswer = s.query(Questions).filter(Questions.uid == uid).first().answer
    mygap = s.query(Questions).filter(Questions.uid == uid).first().gap
    ques = s.query(Questions).filter(Questions.uid == uid).first()
    ques.totol = ques.total + 1
    right = (mytype == 0 or mytype == 2) and answer == myanswer or mytype == 1 and gap == mygap
    new = Records(uid=uid, qid=qid, right=right, rate=0)
    s.add(new)
    # 更新正确率并返回
    records = s.query(Records).filter(Records.uid == uid, Records.qid == qid).all()
    total, true = 0, 0
    for j in records:
        total += 1
        if j.right == 1:
            true += 1
    s.query(Records).filter(Records.uid == uid, Records.qid == qid).all().rate = true / total
    s.commit()
    s.close()
    lis = [right, myanswer, mygap, true / total, ques.right / ques.total]
    return lis
    # 返回值为 是否正确（1为正确，0为错误） 选择题标准答案 填空题标准答案 本题本人正确率 本题整体正确率


# 形成个性化题组
def personalized_recommendation(qnum, chapters_name, choose, gap, user_name):
    # eg.(12,[2,3,4],1,0,168) means 根据168用户的错题记录，生成2、3、4、5章节的12道选择题组
    s = create_session()
    uid = s.query(Stus).filter(Stus.name == user_name).first().uid
    s.commit()
    s.close()
    # 筛选出Records中 该人 该章节 该提醒 的所有错题记录
    records = s.query(Records).filter(Records.uid == uid) \
        .filter(Questions.chapter.in_(chapters_name)) \
        .filter(Questions.type == 1 - choose, Questions.type == gap).all()
    ques = []
    for i in records:
        id = i.qid
        if id not in ques:
            ques.append(id)
    for i in range(len(ques)):
        for j in range(i + 1, len(ques)):
            a = s.query(Records).filter(Records.uid == uid, Records.qid == ques[i]).all().rate
            b = s.query(Records).filter(Records.uid == uid, Records.qid == ques[j]).all().rate
            if a < b:
                ques[i], ques[j] = ques[j], ques[i]
    return ques[0:qnum]
    # 返回问题id


# 返回值是Records行

# 根据id 返回 title, type, answer1, answer2, answer3, answer4
def get_question(qid):
    s = create_session()
    ques = s.query(Questions).filter(Questions.qid == qid).first()
    lis = [ques.title, ques.type, ques.answer,ques.answerA, ques.answerB, ques.answerC, ques.answerD]
    s.commit()
    s.close()
    return lis


if __name__ == '__main__':
    # Base.metadata.create_all(engine)#一键在数据库生成所有的类
    # Base.metadata.delete_all(engine)#一键清除S
    load_one_question('title212', 'answ', 'Chapter 1', 1, 'answer1', 'answer2', 'answer3', 'answer4', 'tab', True,
                      'RRRR')
    # load_one_question(title='hhh',answer=)
    # user_add_into_group(['123', 'hhhhh'], 'stu9')  # 用户主动申请加入