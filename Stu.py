import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.session  # 数据库操作核心
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base  # 父类

Base = declarative_base()
DB_connect = 'mysql+mysqldb://root:1012416935@localhost/Test'
engine = create_engine(DB_connect, echo=False)


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


class Questions(Base):  # 有哪些问题
    __tablename__ = 'questions'
    qid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(1000))
    answer = sqlalchemy.Column(sqlalchemy.String(1000))
    # 用户指定章节,多对多
    chapter = sqlalchemy.orm.relationship("Chapters", secondary=Chap_ques, backref="Ques")
    # 所属问题组，多对多
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary=Ques_qgroup, backref="Ques")


class Stus(Base):
    __tablename__ = 'stus'  # 名字
    uid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    # 进行属性与字段映射，名字可以不一
    name = sqlalchemy.Column(sqlalchemy.String(50))

    password = sqlalchemy.Column(sqlalchemy.String(50))
    # 用户组信息
    groups = sqlalchemy.orm.relationship("Groups", secondary=Stu_group, backref="Stus")
    # 问题组信息
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary=Stu_qgroup, backref="Stus")
    # 格言
    quote = sqlalchemy.Column(sqlalchemy.String(100))
    # 简介
    Bi = sqlalchemy.Column(sqlalchemy.String(100))
    # 这一句是设置多对多的关键地方
    # 第一个参数' '，表示这个关系的另一端是Hero类
    # 第二个参数secondary指向了中间表，中间表只包含关系的两侧表的主键列
    # 第三个参数backref，表示反向引用
    # 是否是超级用户，表示管理员
    issuper = sqlalchemy.Column(sqlalchemy.Boolean)


class Groups(Base):
    __tablename__ = 'groups'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(50))
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创造者
    qgroups = sqlalchemy.orm.relationship("QGroups", secondary=Ggroup_group, backref="Groups")


class QGroups(Base):
    __tablename__ = 'qgroups'
    gid = sqlalchemy.Column(sqlalchemy.BIGINT, primary_key=True)
    uid = sqlalchemy.Column(sqlalchemy.Integer)  # 创造者
    name = sqlalchemy.Column(sqlalchemy.String(20), primary_key=True)


def create_session():  # session用来操作数据库
    session_ = sessionmaker(bind=engine)  # 一个session是一个对数据库链接的包装
    session = session_()  # 实例化session对象
    return session


def check_name(C, name):
    print('a')
    session = create_session()
    print('b')
    # if len(session.query(C).filter(C.name == name).all()) == 0:
    #     print('c')
    #     session.close()
    #     return True
    return True
    print('d')
    session.close()
    print('e')
    return False


# 任务一，个人信息管理
def create_new_user(name, password, issuper):
    # 按下注册确定按键的瞬间,创建新用户
    print('0')
    if check_name(Stus, name) == False:
        print('1')
        pass
        # gui显示名称已被占用
    else:
        print('2')
        new = Stus(name=name, password=password, issuper=issuper)
        s = create_session()
        print('3')
        s.add(new)
        s.commit()
        s.close()


def change_password(password, name):  # 改密码
    s = create_session()
    stu = s.query(Stus).filter(Stus.name == name).first()
    stu.password = password
    s.commit()
    s.close()


def change_name(new, name):  # 改名字，按下确定瞬间
    if check_name(Stus, name) == False:
        pass
        # gui显示名称已被占用
    else:
        s = create_session()
        stu = s.query(Stus).filter(Stus.name == name).first()
        stu.name = name
        s.commit()
        s.close()


def change_quote(new, name):
    s = create_session()
    stu = s.query(Stus).filter(Stus.name == name).first()
    stu.quote = new
    s.commit()
    s.close()


def change_bi(new, name):
    s = create_session()
    stu = s.query(Stus).filter(Stus.name == name).first()
    stu.Bi = new
    s.commit()
    s.close()


# 任务二 管理员创建小组，将他人加入小组，用户搜索加入小组，注意，此时要更新学生的问题组权限
def creat_new_group(g_name, s_name):  # 创建一个空的新的小组
    if check_name(Groups, g_name) == False:
        pass
        # gui显示
    else:
        s = create_session()
        uid = s.query(Stus).filter(Stus.name == s_name).first().uid
        new = Groups(name=g_name, uid=uid)
        s.add(new)
        s.commit()
        s.close()


# 将一组人加进group
def add_into_group(users, g_name):  # 此处users为名字字符串数组
    s = create_session()
    group = s.query(Groups).filter(Groups.name == g_name).first()  # 找到当前学生gruop
    qgroups = group.qgroups  # 当前group的qgroups
    for i in users:
        stu = s.query(Stus).filter(Stus.name == i).first()
        stu.groups.append(group)
        # 这个学生目前的qgroups中不存在的才加入
        for j in qgroups:
            if i in stu.qgroups:
                continue
            stu.qgroups.append(j)
        s.commit()
        s.close()


def not_in_group(gname):
    pass


def delete_from_group(users, gname):  # 将部分人从组里删除
    s = create_session()

    #

    s.commit()
    s.close()


def search_groups(page):
    # 分页显示，每页十条
    s = create_session()
    groups = s.query(Groups).limit(10).offset((page - 1) * 10).all()
    s.close()
    # gui显示


def user_addinto_group(s_name, g_name):  # 用户主动申请加入
    s = create_session()
    stu = s.query(Stus).filter(Stus.name == s_name)
    g = s.query(Groups).filter(Groups.name == g_name)
    stu.groups.append(g)  # 关联的是整个而不是一个值
    s.commit()
    s.close()


# 任务三 上传 单个问题 或 一个文件的问题
def load_one_question(title, answer, chapter):
    # 可以直接加吗？？？
    s = create_session()
    c = s.query(Chapters).filter(Chapters.name == chapter)
    q = Questions(title=title, answer=answer, chapter=c)
    s.add(q)
    s.commit()
    s.close()
    # 分组，给问题加标签


def load_files(path):  # 需要规定文件格式？？再想
    f = open(path, mode='r')
    lines = f.readlines()
    for line in lines:
        # 处理数据
        load_one_question()


def select_chapters(chapters_name):  # 选择哪些chapters
    chapters = []
    s = create_session()
    for i in chapters_name:
        temp = s.query(Chapters).filter(Chapters.name == i)
        chapters.extend(temp)
    return chapters


# 问题共享功能
def create_own_ques_group(qgname, questions):  # 某个用户可以选择构造一个问题组并命名，类比学生和学生组
    s = create_session()
    new = QGroups(name=qgname)
    s.add(new)
    s.commit()
    for i in questions:  # 将选中问题加入问题组中
        temp = s.query(Questions).filter(Questions.qid == i)
        temp.qgroups.append(new)
    s.close()


def share_question_with_groups(qgname, gname):  # 与特定的用户组分享特定的问题组
    s = create_session()
    qid = s.query(Groups).filter(Groups.name == gname).first().gid  # 得到这个用户组的gid
    uids = s.query(Stu_group).filter(Stu_group.gid == qid).all()  # 得到用户组的所有用户的uid
    stus = s.query(Stus).filter(Stus.uid.in_(uids)).all()  # 得到用户组所有用户
    qgroup = s.query(QGroups).filter(QGroups.name == qgname).first()
    for i in stus:
        i.qgroups.append(qgroup)  # 依次建立联系
    s.query(Groups).filter(Groups.name == gname).first().qgroups.append(qgroup)
    s.commit()
    s.close()


if __name__ == '__main__':

    pass
