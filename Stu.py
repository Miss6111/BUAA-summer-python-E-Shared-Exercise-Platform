import sqlalchemy
import openpyxl

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session  # 数据库操作核心
from sqlalchemy.ext.declarative import declarative_base  # 父类
from sqlalchemy import or_, and_, all_, any_

Base = declarative_base()
DB_connect = 'mysql+mysqldb://root:1012416935@localhost/Test'
engine = create_engine(DB_connect, echo=False)


# 评论表
class Comments(Base):
    __tablename__ = 'comments';
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
    ques = sqlalchemy.orm.relationship("Ques", secondary="chap_ques", backref="Chapters", cascade='all')


class Questions(Base):  # 有哪些问题
    __tablename__ = 'questions'
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(1000))
    chapter = sqlalchemy.Column(sqlalchemy.String(10))
    # 所属问题组，多对多
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary="ques_qgroup", backref="Ques", cascade='all')
    # 题型,0选择，1填空
    type = sqlalchemy.Column(sqlalchemy.Integer)
    # ”1010“为选AC
    answer = sqlalchemy.Column(sqlalchemy.String(5))
    # ABCD四个选项，填空默认显示A
    answerA = sqlalchemy.Column(sqlalchemy.String(100))
    answerB = sqlalchemy.Column(sqlalchemy.String(100))
    answerC = sqlalchemy.Column(sqlalchemy.String(100))
    answerD = sqlalchemy.Column(sqlalchemy.String(100))
    public = sqlalchemy.Column(sqlalchemy.Boolean)


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
    starquestions = sqlalchemy.orm.relationship("Questions", secondary="Star_stu", backref="Stus", cascade='all')
    # 格言
    quote = sqlalchemy.Column(sqlalchemy.String(100))
    # 简介
    Bi = sqlalchemy.Column(sqlalchemy.String(100))
    issuper = sqlalchemy.Column(sqlalchemy.Boolean)
    hasnew = sqlalchemy.Column(sqlalchemy.Boolean)


Stu_now = ""  # 存当前正在操作的学生的名字，是一个字符串，-->重命名记得改
Stu_now_id = 0;


class Groups(Base):
    __tablename__ = 'groups'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创造者
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary="qgroup_group", backref="Groups")


class QGroups(Base):
    __tablename__ = 'qgroups'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创造者
    name = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)


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
def create_new_user(name, password, super):  # 按下注册确定按键的瞬间,创建新用户
    """

    :param name:
    :param password:
    :param super:
    :return:
    """
    s = create_session()
    if not check_name(Stus, name):
        return False
    else:
        new = Stus(name=name, password=password, issuper=super, Bi="你还没有写任何简介", quote="", groups=[], qgroups=[])
        s.add(new)
        s.commit()
        s.close()
        return True


def change_password(password):  # 改密码
    """

    :param password:
    """
    s = create_session()
    s.query(Stus).filter(Stus.name == Stu_now).first().password = password
    s.commit()
    s.close()


def change_name(new):  # 改名字，按下确定瞬间
    """

    :param new:
    :return:
    """
    if not check_name(Stus, new):
        return False
    else:
        s = create_session()
        s.query(Stus).filter(Stus.name == Stu_now).first().name = new
        s.commit()
        s.close()
        return True


def change_quote(new):  # 改格言
    """

    :param new:
    """
    s = create_session()
    s.query(Stus).filter(Stus.name == Stu_now).first().quote = new
    s.commit()
    s.close()


def change_bi(new):  # 改简介
    """

    :param new:
    """
    s = create_session()
    s.query(Stus).filter(Stus.name == Stu_now).first().Bi = new
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
            global Stu_now
            Stu_now = s.query(Stus).filter(Stus.name == name).first().name
            s.close()
            return True
        else:
            s.close()
            return False


# 任务二 管理员创建小组，将他人加入小组，用户搜索加入小组，注意，此时要更新学生的问题组权限
def check_super():
    """

    :return: 
    """
    s = create_session()
    return s.query(Stus).filter(Stus.name == Stu_now).first().issuper


def create_new_group(g_name):  # 创建一个空的新的小组(小组名)
    """

    :param g_name: 
    :return: 
    """
    s = create_session()
    if not check_name(Groups, g_name):  # 名字存在
        s.close()
        return False
    elif s.query(Stus).filter(Stus.name == Stu_now).first().issuper == 0:
        s.close()
        return False
    else:
        uid = s.query(Stus).filter(Stus.name == Stu_now).first().uid
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
    group = s.query(Groups).filter(Groups.name == g_name).first()  # 找到当前学生gruop
    qgroups = group.qgroups  # 当前group的qgroups

    for i in users:  # 遍历每一个学生
        stu = s.query(Stus).filter(Stus.name == i).first()
        stu.groups.append(group)  # 保证此时学生一定不在这个组
        # 这个学生目前的qgroups中不存在的才加入
        for j in qgroups:
            if j in stu.qgroups:
                continue
            stu.qgroups.append(j)  # 学生加入权限
    s.commit()
    s.close()


def not_in_group(gname, page):  # 选择学生加入时，能显示出来的都是不在这个组里的,page表分页显示的第几页
    """

    :param gname:
    :param page:
    :return:
    """
    s = create_session()
    gid = s.query(Groups).filter(Groups.name == gname).first().gid
    uids = s.query(Stu_group).filter(Stu_group.gid != gid).limit(10).offset((page - 1) * 10).all()
    unames = []
    for i in uids:
        unames.append(s.query(Stus).filter(Stus.uid == i).first().name)
    # 返回值是这一页的所有学生名字
    s.commit()
    s.close()
    return unames


def delete_from_group(users, gname):  # 将部分人从组里删除
    """

    :param users:
    :param gname:
    """
    s = create_session()
    group = s.query(Groups).filter(Groups.name == gname).first()
    qgroups = group.qgroups
    for i in users:
        user = s.query(Stus).filter(Stus.name == i).first()
        user.groups.remove(group)
        for j in qgroups:
            user.groups.remove(j)
    s.commit()
    s.close()


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


def user_add_into_group(g_name):  # 用户主动申请加入
    """

    :param g_name:
    :return:
    """
    s = create_session()
    # 如果已经在组里，加入失败
    uid = s.query(Stus).filter(Stus.name == Stu_now).first().uid
    group = s.query(Groups).filter(Groups.name == g_name).first()
    gid = group.gid
    if gid in s.query(Stu_group).filter(Stu_group.uid == uid).all():
        s.close()
        return False
    # 加入成功
    stu = s.query(Stus).filter(Stus.name == Stu_now).first()
    stu.groups.append(group)  # 关联的是整个而不是一个值

    qgroups = group.qgroups  # 当前group的qgroups
    # 这个学生目前的qgroups中不存在的才加入
    for j in qgroups:
        if j in stu.qgroups:
            continue
        stu.qgroups.append(j)  # 学生加入权限
    s.commit()
    s.close()


# 任务三 上传 单个问题 或 一个文件的问题
def show_all_chapter():
    """

    :return:
    """
    s = create_session()
    return s.query(Chapters.name).all()  # 看一下是否切实满足返回名字集合


def load_one_question(title, answer, chapter, my_type, answer1, answer2, answer3, answer4, public):
    """


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
    q = Questions(title=title, answer=answer, type=my_type, answer1=answer1, answer2=answer2, answer3=answer3,
                  answer4=answer4, public=public)
    s.add(q)
    s.commit()
    c.ques.append(q)
    s.commit()
    s.close()
    # 分组，给问题加标签


def load_files(path):  # 需要规定文件格式？？再想
    """

    :param path:
    """
    f = openpyxl.load_workbook(path)
    names = f.get_sheet_names()  # 所有sheet
    for sheet_name in names:  # 每一页
        sheet = f.get_sheet_by_name(sheet_name)
        rows = sheet.max_row
        for i in range(rows):  # 每一行是一个问题
            title = sheet.cell(i + 1, 1).value
            answer = sheet.cell(i + 1, 2).value
            chapter = sheet.cell(i + 1, 3).value
            mytype = sheet.cell(i + 1, 4).value
            answer1 = sheet.cell(i + 1, 5).value
            answer2 = sheet.cell(i + 1, 6).value
            answer3 = sheet.cell(i + 1, 7).value
            answer4 = sheet.cell(i + 1, 8).value
            # 默认是公开的
            load_one_question(title, answer, chapter, mytype, answer1, answer2, answer3, answer4, public=True)
            s = create_session()


def select_questions(chapters_name, mytype):  # 选择哪些chapters,填空,选择,权限
    """

    :param chapters_name:
    :param type:
    :return:
    """
    s = create_session()
    q = s.query(Questions).filter(or_(Questions.chapter.in_(chapters_name), Questions.public == True)).filter(
        Questions.type == mytype).all()
    groups = s.query(Stus).filter(Stus.name == Stu_now).first().groups
    gids = []  # 用户在的所有组
    for i in groups:
        gids.append(i.gid)

    questions = []
    for i in q:  # 遍历每个问题
        qgids = []  # 问题属于的问题组
        for j in i.qgroups:
            qgids.append(j.gid)
        if len(s.query(Ggroup_group).filter(Ggroup_group.gid.in_(gids)).filter(
                Ggroup_group.qgid.in_(qgids)).all()) != 0:
            questions.append(i)

    s.close()
    # 返回值是所有符合要求的问题
    return questions


# 问题共享功能
def create_own_ques_group(name):  # 某个用户可以选择构造一个问题组并命名，类比学生和学生组
    """

    :param name:
    :return:
    """
    if check_name(QGroups, name) == False:
        return False
    s = create_session()
    uid = s.query(Stus).filter(Stus.name == Stu_now).first().uid
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
def send_comments(qid, content):
    """

    :param qid:
    :param content:
    """
    s = create_session()
    stu = s.query(Stus).filter(Stus.name == Stu_now).first()
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


def search_for_sen():
    """
:return
    """
    pass


def generate_talent_tabel():
    """
:return
    """
    # 日期和错题记录
    pass


def search_star_questions(page):  #
    """

    :param page: 
    :return: 
    """
    # 分页显示，每页十条
    s = create_session()
    temps = s.query(Star_stu).filter(Star_stu.uid == Stu_now_id).limit(10).offset((page - 1) * 10).all()
    questions = []
    for i in temps:
        questions.append(s.query(Questions).filter(Questions.qid == i.qid).first())
    s.close()
    # 返回值是存有问题的数组
    return questions


if __name__ == '__main__':
    # Base.metadata.create_all(engine)#一键在数据库生成所有的类
    # Base.metadata.drop_all(engine)#一键清除
    pass
