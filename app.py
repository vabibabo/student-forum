
from flask import Flask, render_template, request, redirect, url_for, session, g, flash, jsonify, Response
import config
from exts import db
from models import User, Topic, Claim, Reply
from decorator import login_required
from sqlalchemy import or_
from werkzeug.routing import BaseConverter
from datetime import datetime
import pymysql
from flask_bootstrap import Bootstrap




pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
bootstrap = Bootstrap(app)




# 用户在访问/posts/a+b
class ListConveter(BaseConverter):
    # 把参数a+b等内容，根据“+”进行切割，形成列表
    def to_python(self, value):
        return value.split("+")

    # 把url_for的参数反转结果自动拼接为a+b的形式
    def to_url(self, value):
        return "+".join(value)

# 添加转换器
app.url_map.converters['arr'] = ListConveter

class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        """
        这个方法只有视图函数返回非字符串、非元祖、非Response对象才会调用。
        :param response:
        :param environ:
        :return:
        """
        # 将字典转化为json格式
        if isinstance(response, dict):
            response = jsonify(response)
        return super(JSONResponse, cls).force_type(response, environ)

app.response_class = JSONResponse


@app.route('/')
@app.route('/index/')
def index():

    return render_template('index.html')



@app.route('/detail/<topic_id>/')
def detail(topic_id):
    context = {
        'topic': Topic.query.filter(Topic.id == topic_id).first()
    }
    return render_template('detail.html',**context)



@app.route('/add_claim/',methods=['POST'])
@login_required
def add_claim():
    title = request.form.get('claim_title')
    content = request.form.get('claim_content')
    topic_id = request.form.get('topic_id')
    claim = Claim(content=content)
    # 生成回答者对应关系
    claim.author = g.user
    # 生成问题对应关系
    topic = Topic.query.filter(Topic.id == topic_id).first()
    claim.topic = topic
    # 保存数据
    db.session.add(claim)
    db.session.commit()

    return redirect(url_for('detail',topic_id=topic_id))
@app.route('/add_reply/',methods=['POST'])
@login_required
def add_reply():
    content = request.form.get('reply_content')
    claim_id = request.form.get('claim_id')
    reply = Reply(content=content)
    # 生成回答者对应关系
    reply.author = g.user
    # 生成问题对应关系
    claim = Claim.query.filter(Claim.id == claim_id).first()
    reply.claim = claim
    # 保存数据
    db.session.add(reply)
    db.session.commit()

    return redirect(url_for('reply',claim_id=claim_id))

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 数据有效性校验
        if username == '':
            flash(u'Username can not be empty!')
            return render_template('regist.html')

        if password1 == '' or password2 == '':
            flash(u'Password can not be empty!')
            return render_template('regist.html')
        user = User.query.filter(User.username == username).first()
        if user:
            flash(u'The username is already registered')
            return render_template('regist.html')
        else:
            if password1 != password2:
                flash(u'The two passwords are not equal, please check and fill in again ')
                return render_template('regist.html')

            else:
                user = User(username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        # 数据有效性校验
        if username == '':
            flash(u'Can not empty')
            return render_template('login.html')

        if password == '':
            flash(u'Can not empty')
            return render_template('login.html')


        # 登录处理
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash(u'User name not correct')
            return render_template('login.html')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/topic/',methods=['GET','POST'])
@login_required
def topic():
    if request.method == 'GET':
        return render_template('topic.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        if title == '':
            return u'Title can not be empty'
        if content == '':
            return u'Content can not be empty'
        topic = Topic(title=title, content=content)
        topic.author = g.user
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/search/')
def search():
    q = request.args.get('q')
    # 或(or)查询
    where = or_(Topic.title.contains(q),Topic.content.contains(q))
    topics = Topic.query.filter(where).order_by('-create_time')
    # 与(and)查询
    # questions = Question.query.filter(Question.title.contains(q),Question.content.contains(q)).order_by('-create_time')
    return render_template('index.html', topics=topics, q=q)

@app.route('/posts/<arr:boards>')
def posts(boards):
    # to_url()
    print(url_for('posts', boards=['a', 'b']))
    # to_python()
    return "%s" % boards


# jinjia2自定义过滤器（时间）
@app.template_filter('handle_time')
def handle_time(time):
    """
    time距离现在的时间间隔：
    1、如果时间间隔小于1分钟以内，那么就显示“刚刚”
    2、如果是大于1分钟小于1小时，那么就显示“XX分钟前”
    3、如果是大于1小时小于24小时，那么就显示“XX小时前”
    4、如果是大于24小时小于30天以内，那么就显示“XX天前”
    5、否则就是显示具体的时间
    :param time:
    :return:
    """
    if isinstance(time, datetime):
        now = datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return u"刚刚"
        elif timestamp >= 60 and timestamp < 3600:
            minutes = timestamp / 60
            return u"%s分钟前" % int(minutes)
        elif timestamp >= 3600 and timestamp < 86400:
            hours = timestamp / 3600
            return u"%s小时前" % int(hours)
        elif timestamp >= 86400 and timestamp < 2592000:
            day = timestamp / 86400
            return u"%s天前" % int(day)
        else:
            return time.strftime('%Y/%m/%d %H:%M')
    else:
        return time




@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    """
    上下文处理器（context_processor），必须要返回一个字典。假如返回内容为空，那也要返回一个空字典！
    :return: user信息
    """
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

if __name__ == '__main__':

    app.config['TEMPLATES_AUTO_RELOADE'] = True

    app.run()

