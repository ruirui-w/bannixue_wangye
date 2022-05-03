from flask import Flask
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask import request
from config import Config#从config模块导入Config类
from flask_sqlalchemy import SQLAlchemy#从包中导入类
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel,lazy_gettext as _l
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('请登录以浏览')
mail = Mail(app)
moment = Moment(app)
babel = Babel(app)


db = SQLAlchemy(app)#数据库对象
migrate = Migrate(app, db)#迁移引擎对象

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

from app import routes,models,errors#导入一个新模块models，它将定义数据库的结构，目前为止尚未编写