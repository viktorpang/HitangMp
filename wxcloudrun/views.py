from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import (
    delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid,
    query_poetry_by_keyword, query_poetry_by_author, query_random_poetry, insert_poetry,
    query_character_etymology, query_characters_by_radical, query_characters_by_stroke_count, insert_character_etymology,
    query_calendar_knowledge_by_category, insert_calendar_knowledge,
    query_astronomy_knowledge_by_constellation, insert_astronomy_knowledge,
    query_cultural_knowledge_by_category, query_random_cultural_knowledge, insert_cultural_knowledge
)
from wxcloudrun.model import Counters, Poetry, CharacterEtymology, CalendarKnowledge, AstronomyKnowledge, CulturalKnowledge
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


# 诗词相关API
@app.route('/api/poetry/search', methods=['GET'])
def search_poetry():
    """搜索诗词"""
    keyword = request.args.get('keyword', '')
    author = request.args.get('author', '')
    
    if keyword:
        poems = query_poetry_by_keyword(keyword)
    elif author:
        poems = query_poetry_by_author(author)
    else:
        poems = []
    
    result = []
    for poem in poems:
        result.append({
            'id': poem.id,
            'title': poem.title,
            'author': poem.author,
            'dynasty': poem.dynasty,
            'content': poem.content,
            'tags': poem.tags
        })
    
    return make_succ_response(result)


@app.route('/api/poetry/random', methods=['GET'])
def get_random_poetry():
    """获取随机诗词"""
    poem = query_random_poetry()
    if poem:
        result = {
            'id': poem.id,
            'title': poem.title,
            'author': poem.author,
            'dynasty': poem.dynasty,
            'content': poem.content,
            'tags': poem.tags
        }
        return make_succ_response(result)
    return make_succ_response(None)


@app.route('/api/poetry/add', methods=['POST'])
def add_poetry():
    """添加诗词"""
    data = request.get_json()
    try:
        poetry = Poetry(
            title=data['title'],
            author=data['author'],
            dynasty=data['dynasty'],
            content=data['content'],
            tags=data.get('tags', '')
        )
        insert_poetry(poetry)
        return make_succ_response({'id': poetry.id})
    except Exception as e:
        return make_err_response(str(e))


# 汉字字源相关API
@app.route('/api/etymology/search', methods=['GET'])
def search_character_etymology():
    """查询单个汉字的字源信息"""
    character = request.args.get('character', '')
    
    if not character:
        return make_err_response('请输入要查询的汉字')
    
    if len(character) > 1:
        return make_err_response('只能查询单个汉字')
    
    etymology = query_character_etymology(character)
    if etymology:
        result = {
            'id': etymology.id,
            'character': etymology.character,
            'pinyin': etymology.pinyin,
            'radical': etymology.radical,
            'stroke_count': etymology.stroke_count,
            'etymology': etymology.etymology,
            'ancient_forms': etymology.ancient_forms,
            'meaning': etymology.meaning,
            'extended_meanings': etymology.extended_meanings,
            'examples': etymology.examples,
            'stroke_order': etymology.stroke_order,
            'dictionary_source': etymology.dictionary_source
        }
        return make_succ_response(result)
    else:
        return make_succ_response(None)


@app.route('/api/etymology/radical', methods=['GET'])
def get_characters_by_radical():
    """按部首查询汉字"""
    radical = request.args.get('radical', '')
    
    if not radical:
        return make_err_response('请输入部首')
    
    characters = query_characters_by_radical(radical)
    result = []
    for char in characters:
        result.append({
            'id': char.id,
            'character': char.character,
            'pinyin': char.pinyin,
            'radical': char.radical,
            'stroke_count': char.stroke_count,
            'meaning': char.meaning
        })
    
    return make_succ_response(result)


@app.route('/api/etymology/strokes', methods=['GET'])
def get_characters_by_stroke_count():
    """按笔画数查询汉字"""
    stroke_count = request.args.get('count', '')
    
    if not stroke_count or not stroke_count.isdigit():
        return make_err_response('请输入有效的笔画数')
    
    characters = query_characters_by_stroke_count(int(stroke_count))
    result = []
    for char in characters:
        result.append({
            'id': char.id,
            'character': char.character,
            'pinyin': char.pinyin,
            'radical': char.radical,
            'stroke_count': char.stroke_count,
            'meaning': char.meaning
        })
    
    return make_succ_response(result)


@app.route('/api/etymology/add', methods=['POST'])
def add_character_etymology():
    """添加汉字字源信息"""
    data = request.get_json()
    try:
        etymology = CharacterEtymology(
            character=data['character'],
            pinyin=data.get('pinyin', ''),
            radical=data.get('radical', ''),
            stroke_count=data.get('stroke_count', 0),
            etymology=data.get('etymology', ''),
            ancient_forms=data.get('ancient_forms', ''),
            meaning=data.get('meaning', ''),
            extended_meanings=data.get('extended_meanings', ''),
            examples=data.get('examples', ''),
            stroke_order=data.get('stroke_order', ''),
            dictionary_source=data.get('dictionary_source', '')
        )
        insert_character_etymology(etymology)
        return make_succ_response({'id': etymology.id})
    except Exception as e:
        return make_err_response(str(e))


# 历法知识相关API
@app.route('/api/calendar/solar-terms', methods=['GET'])
def get_solar_terms():
    """获取节气信息"""
    solar_terms = query_calendar_knowledge_by_category('节气')
    result = []
    for term in solar_terms:
        result.append({
            'id': term.id,
            'title': term.title,
            'content': term.content,
            'date_info': term.date_info
        })
    return make_succ_response(result)


@app.route('/api/calendar/festivals', methods=['GET'])
def get_festivals():
    """获取传统节日"""
    festivals = query_calendar_knowledge_by_category('节日')
    result = []
    for festival in festivals:
        result.append({
            'id': festival.id,
            'title': festival.title,
            'content': festival.content,
            'date_info': festival.date_info
        })
    return make_succ_response(result)


@app.route('/api/calendar/add', methods=['POST'])
def add_calendar_knowledge():
    """添加历法知识"""
    data = request.get_json()
    try:
        knowledge = CalendarKnowledge(
            title=data['title'],
            content=data['content'],
            category=data.get('category', ''),
            date_info=data.get('date_info', '')
        )
        insert_calendar_knowledge(knowledge)
        return make_succ_response({'id': knowledge.id})
    except Exception as e:
        return make_err_response(str(e))


# 天文知识相关API
@app.route('/api/astronomy/constellations', methods=['GET'])
def get_constellations():
    """获取星宿信息"""
    constellation = request.args.get('constellation', '')
    if constellation:
        knowledge = query_astronomy_knowledge_by_constellation(constellation)
    else:
        knowledge = []
    
    result = []
    for item in knowledge:
        result.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'constellation': item.constellation,
            'period': item.period
        })
    return make_succ_response(result)


@app.route('/api/astronomy/add', methods=['POST'])
def add_astronomy_knowledge():
    """添加天文知识"""
    data = request.get_json()
    try:
        knowledge = AstronomyKnowledge(
            title=data['title'],
            content=data['content'],
            constellation=data.get('constellation', ''),
            period=data.get('period', '')
        )
        insert_astronomy_knowledge(knowledge)
        return make_succ_response({'id': knowledge.id})
    except Exception as e:
        return make_err_response(str(e))


# 文化百科相关API
@app.route('/api/culture/daily', methods=['GET'])
def get_daily_culture():
    """获取每日文化知识"""
    knowledge = query_random_cultural_knowledge()
    if knowledge:
        result = {
            'id': knowledge.id,
            'title': knowledge.title,
            'content': knowledge.content,
            'category': knowledge.category,
            'tags': knowledge.tags
        }
        return make_succ_response(result)
    return make_succ_response(None)


@app.route('/api/culture/category', methods=['GET'])
def get_culture_by_category():
    """根据分类获取文化知识"""
    category = request.args.get('category', '')
    knowledge = query_cultural_knowledge_by_category(category)
    
    result = []
    for item in knowledge:
        result.append({
            'id': item.id,
            'title': item.title,
            'content': item.content,
            'category': item.category,
            'tags': item.tags
        })
    return make_succ_response(result)


@app.route('/api/culture/add', methods=['POST'])
def add_cultural_knowledge():
    """添加文化知识"""
    data = request.get_json()
    try:
        knowledge = CulturalKnowledge(
            title=data['title'],
            content=data['content'],
            category=data.get('category', ''),
            tags=data.get('tags', '')
        )
        insert_cultural_knowledge(knowledge)
        return make_succ_response({'id': knowledge.id})
    except Exception as e:
        return make_err_response(str(e))


# 数据初始化API
@app.route('/api/init-data', methods=['POST'])
def init_data():
    """初始化示例数据"""
    try:
        # 添加示例诗词
        sample_poems = [
            {
                'title': '静夜思',
                'author': '李白',
                'dynasty': '唐',
                'content': '床前明月光，疑是地上霜。举头望明月，低头思故乡。',
                'tags': '思乡,月亮'
            },
            {
                'title': '春晓',
                'author': '孟浩然',
                'dynasty': '唐',
                'content': '春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。',
                'tags': '春天,自然'
            }
        ]
        
        for poem_data in sample_poems:
            poetry = Poetry(**poem_data)
            insert_poetry(poetry)
        
        # 添加示例汉字字源数据
        sample_etymology = [
            {
                'character': '爱',
                'pinyin': 'ài',
                'radical': '爪',
                'stroke_count': 10,
                'etymology': '爱字从爪从心，表示用心去抓取、呵护。古文字中，爪表示手，心表示情感，合起来表示用心去关爱。',
                'ancient_forms': '甲骨文：𢆶 金文：愛 小篆：愛',
                'meaning': '喜爱、关爱',
                'extended_meanings': '爱护、爱惜、爱慕',
                'examples': '爱心、爱情、爱国',
                'stroke_order': '撇、点、点、撇、点、横钩、竖、横折、横、横',
                'dictionary_source': '说文解字、康熙字典'
            },
            {
                'character': '国',
                'pinyin': 'guó',
                'radical': '囗',
                'stroke_count': 8,
                'etymology': '国字从囗从玉，表示有城墙包围的珍宝之地。囗表示城墙，玉表示珍贵之物，合起来表示国家。',
                'ancient_forms': '甲骨文：囗 金文：國 小篆：國',
                'meaning': '国家、邦国',
                'extended_meanings': '国度、国土、国人',
                'examples': '国家、国际、祖国',
                'stroke_order': '竖、横折、横、横、竖、横折、横、横',
                'dictionary_source': '说文解字、康熙字典'
            },
            {
                'character': '学',
                'pinyin': 'xué',
                'radical': '子',
                'stroke_count': 8,
                'etymology': '学字从爻从子，表示孩子在模仿学习。爻表示交错变化，子表示孩子，合起来表示孩子通过模仿来学习。',
                'ancient_forms': '甲骨文：𡥼 金文：學 小篆：學',
                'meaning': '学习、模仿',
                'extended_meanings': '学问、学校、学问',
                'examples': '学习、学校、学问',
                'stroke_order': '点、点、撇、点、撇、横钩、竖、横',
                'dictionary_source': '说文解字、康熙字典'
            }
        ]
        
        for etymology_data in sample_etymology:
            etymology = CharacterEtymology(**etymology_data)
            insert_character_etymology(etymology)
        
        return make_succ_response({'message': '数据初始化成功'})
    except Exception as e:
        return make_err_response(str(e))
