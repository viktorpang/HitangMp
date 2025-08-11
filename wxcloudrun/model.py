from datetime import datetime

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 诗词表
class Poetry(db.Model):
    __tablename__ = 'Poetry'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # 诗题
    author = db.Column(db.String(50), nullable=False)   # 作者
    dynasty = db.Column(db.String(20), nullable=False)  # 朝代
    content = db.Column(db.Text, nullable=False)        # 诗词内容
    tags = db.Column(db.String(200))                    # 标签
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 汉字字源表
class CharacterEtymology(db.Model):
    __tablename__ = 'CharacterEtymology'
    
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(10), nullable=False)     # 汉字
    pinyin = db.Column(db.String(50))                        # 拼音
    radical = db.Column(db.String(20))                       # 部首
    stroke_count = db.Column(db.Integer)                     # 笔画数
    etymology = db.Column(db.Text)                          # 字源解释
    ancient_forms = db.Column(db.Text)                      # 古文字形态
    meaning = db.Column(db.Text)                            # 本义
    extended_meanings = db.Column(db.Text)                  # 引申义
    examples = db.Column(db.Text)                           # 例词例句
    stroke_order = db.Column(db.Text)                       # 笔顺说明
    dictionary_source = db.Column(db.String(100))           # 字典来源
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 历法知识表
class CalendarKnowledge(db.Model):
    __tablename__ = 'CalendarKnowledge'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)       # 标题
    content = db.Column(db.Text, nullable=False)            # 内容
    category = db.Column(db.String(50))                     # 分类（节气、节日等）
    date_info = db.Column(db.String(50))                    # 日期信息
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 天文知识表
class AstronomyKnowledge(db.Model):
    __tablename__ = 'AstronomyKnowledge'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)       # 标题
    content = db.Column(db.Text, nullable=False)            # 内容
    constellation = db.Column(db.String(50))                # 星宿
    period = db.Column(db.String(50))                      # 时期
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 文化百科表
class CulturalKnowledge(db.Model):
    __tablename__ = 'CulturalKnowledge'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)       # 标题
    content = db.Column(db.Text, nullable=False)            # 内容
    category = db.Column(db.String(50))                     # 分类
    tags = db.Column(db.String(200))                       # 标签
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())
