from flask import Flask, url_for
from flask_mail import Mail, Message


from werkzeug.utils import redirect

app = Flask(__name__)
app.config.update(dict(
    Debug=True,
    MAIL_SERVER='smtp.163.com',
    MAIL_POST=25,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='ruirui__ww@163.com',
    MAIL_PASSWORD='KPLYKRTGJLJGIWKQ'
))
mail=Mail(app)
@app.route('/')
def hello_():
    return 'Hello'
@app.route('/send_mail')
def send_mail():
    msg=Message('hello',sender=app.config['MAIL_USERNAME'],recipients=['1569428479@qq.com'])
    msg.body='世事难料'
    print(msg)
    mail.send(msg)
    return redirect(url_for('hello_'))
if __name__ == '__main__':
    app.run()
