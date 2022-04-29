from flask import Flask  # 从flask包中导入Flask类

from config import Config#从init代表了app,config模块导入Config类
app = Flask(__name__)  # 将Flask类的实例 赋值给名为 app 的变量。这个实例成为app包的成员。
app.config.from_object(Config)
print(app.config['SECRET_KEY'])
from app import routes  # 从app包中导入模块routes #先执行其他语句
