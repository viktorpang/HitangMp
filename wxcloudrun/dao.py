import logging

from sqlalchemy.exc import OperationalError
from sqlalchemy import or_, and_

from wxcloudrun import db
from wxcloudrun.model import Counters, Poetry, CharacterEtymology, CalendarKnowledge, AstronomyKnowledge, CulturalKnowledge

# 初始化日志
logger = logging.getLogger('log')


def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


# 诗词相关DAO函数
def query_poetry_by_keyword(keyword):
    """根据关键词搜索诗词"""
    try:
        return Poetry.query.filter(
            or_(
                Poetry.title.contains(keyword),
                Poetry.author.contains(keyword),
                Poetry.content.contains(keyword),
                Poetry.tags.contains(keyword)
            )
        ).all()
    except OperationalError as e:
        logger.info("query_poetry_by_keyword errorMsg= {} ".format(e))
        return None


def query_poetry_by_author(author):
    """根据作者搜索诗词"""
    try:
        return Poetry.query.filter(Poetry.author.contains(author)).all()
    except OperationalError as e:
        logger.info("query_poetry_by_author errorMsg= {} ".format(e))
        return None


def query_random_poetry():
    """获取随机诗词"""
    try:
        return Poetry.query.order_by(db.func.rand()).first()
    except OperationalError as e:
        logger.info("query_random_poetry errorMsg= {} ".format(e))
        return None


def insert_poetry(poetry):
    """插入诗词"""
    try:
        db.session.add(poetry)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_poetry errorMsg= {} ".format(e))


# 汉字字源相关DAO函数
def query_character_etymology(character):
    """查询单个汉字的字源信息"""
    try:
        return CharacterEtymology.query.filter(CharacterEtymology.character == character).first()
    except OperationalError as e:
        logger.info("query_character_etymology errorMsg= {} ".format(e))
        return None


def query_characters_by_radical(radical):
    """按部首查询汉字"""
    try:
        return CharacterEtymology.query.filter(CharacterEtymology.radical == radical).all()
    except OperationalError as e:
        logger.info("query_characters_by_radical errorMsg= {} ".format(e))
        return None


def query_characters_by_stroke_count(stroke_count):
    """按笔画数查询汉字"""
    try:
        return CharacterEtymology.query.filter(CharacterEtymology.stroke_count == stroke_count).all()
    except OperationalError as e:
        logger.info("query_characters_by_stroke_count errorMsg= {} ".format(e))
        return None


def insert_character_etymology(etymology):
    """插入汉字字源信息"""
    try:
        db.session.add(etymology)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_character_etymology errorMsg= {} ".format(e))


# 历法知识相关DAO函数
def query_calendar_knowledge_by_category(category):
    """根据分类查询历法知识"""
    try:
        return CalendarKnowledge.query.filter(CalendarKnowledge.category == category).all()
    except OperationalError as e:
        logger.info("query_calendar_knowledge_by_category errorMsg= {} ".format(e))
        return None


def insert_calendar_knowledge(knowledge):
    """插入历法知识"""
    try:
        db.session.add(knowledge)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_calendar_knowledge errorMsg= {} ".format(e))


# 天文知识相关DAO函数
def query_astronomy_knowledge_by_constellation(constellation):
    """根据星宿查询天文知识"""
    try:
        return AstronomyKnowledge.query.filter(AstronomyKnowledge.constellation == constellation).all()
    except OperationalError as e:
        logger.info("query_astronomy_knowledge_by_constellation errorMsg= {} ".format(e))
        return None


def insert_astronomy_knowledge(knowledge):
    """插入天文知识"""
    try:
        db.session.add(knowledge)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_astronomy_knowledge errorMsg= {} ".format(e))


# 文化百科相关DAO函数
def query_cultural_knowledge_by_category(category):
    """根据分类查询文化知识"""
    try:
        return CulturalKnowledge.query.filter(CulturalKnowledge.category == category).all()
    except OperationalError as e:
        logger.info("query_cultural_knowledge_by_category errorMsg= {} ".format(e))
        return None


def query_random_cultural_knowledge():
    """获取随机文化知识"""
    try:
        return CulturalKnowledge.query.order_by(db.func.rand()).first()
    except OperationalError as e:
        logger.info("query_random_cultural_knowledge errorMsg= {} ".format(e))
        return None


def insert_cultural_knowledge(knowledge):
    """插入文化知识"""
    try:
        db.session.add(knowledge)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_cultural_knowledge errorMsg= {} ".format(e))
