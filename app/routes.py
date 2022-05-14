from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app import app  # 从app包中导入 app这个实例
from app.models import User, Post
# 2个路由
from werkzeug.urls import url_parse
from flask_babel import _
from app.forms import LoginForm, EditProfileForm, PostForm
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from datetime import datetime
from app import db
from app.forms import RegistrationForm
from app.forms import PostForm
from app.models import Post
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm
import numpy as np
''''''
import cv2
import matplotlib
from matplotlib import pyplot as plt
import time
import winsound

face_cascade = cv2.CascadeClassifier('D:/pycharm/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
Leye_cascade = cv2.CascadeClassifier('D:/pycharm/Lib/site-packages/cv2/data/haarcascade_lefteye_2splits.xml')
Reye_cascade = cv2.CascadeClassifier('D:/pycharm/Lib/site-packages/cv2/data/haarcascade_righteye_2splits.xml')
eye_cascade = cv2.CascadeClassifier('D:/pycharm/Lib/site-packages/cv2/data/haarcascade_eye.xml')

simulate_real_time = "true"

process_eye = 0
eyeq_len = 5
eyeq = []
def push_val(val):
    if (val < 800):
        if len(eyeq) <= eyeq_len:
            eyeq.append(val)
        else:
            eyeq.append(val)
            eyeq.pop(0)
    return avg_eyeq()


def avg_eyeq():
    # calculate average
    avg = 0
    for i in eyeq:
        avg = avg + i
    avg = avg / (len(eyeq)+1)

    return avg


def detect_and_draw(img, gray):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[int((y + h / 4)):int((y + 0.55 * h)), int((x + 0.13 * w)):int((x + w - 0.13 * w))]
        roi_color = img[int((y + h / 4)):int((y + 0.55 * h)), int((x + 0.13 * w)):int((x + w - 0.13 * w))]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        max_eyes = 2
        cnt_eye = 0
        for (ex, ey, ew, eh) in eyes:
            if (cnt_eye == max_eyes):
                break;

            image_name = 'Eye_' + str(cnt_eye)
            # print image_name

            # change dimentionas
            # ex = ex + (ew/6)
            # ew = ew - (ew/6)
            # ey = ey + (eh/3)
            # eh = eh/3

            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

            roi_eye_gray = roi_gray[ey:ey + eh, ex:ex + ew]
            roi_eye_color = roi_color[ey:ey + eh, ex:ex + ew]

            # create & normalize histogram ---------
            hist = cv2.calcHist([roi_eye_gray], [0], None, [256], [0, 256])
            histn = []
            max_val = 0
            for i in hist:
                value = int(i[0])
                histn.append(value)
                if (value > max_val):
                    max_val = value
            for index, value in enumerate(histn):
                histn[index] = ((value * 256) / max_val)

            threshold = np.argmax(histn)
            # print histn
            # normalize histogram ends ---------

            # Slice
            roi_eye_gray2 = roi_eye_gray.copy()
            # roi_eye_gray2 = cv2.threshold(roi_eye_gray2, 50, 255, cv2.THRESH_TOZERO)
            # roi_eye_gray2 = cv2.adaptiveThreshold(roi_eye_gray2, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 10)

            total_white = 0
            total_black = 0
            for i in range(0, roi_eye_gray2.shape[0]):
                for j in range(0, roi_eye_gray2.shape[1]):
                    pixel_value = roi_eye_gray2[i, j]
                    if (pixel_value >= threshold):
                        roi_eye_gray2[i, j] = 255
                        total_white = total_white + 1
                    else:
                        roi_eye_gray2[i, j] = 0
                        total_black = total_black + 1

            binary = cv2.resize(roi_eye_gray2, None, fx=2, fy=2)
            #cv2.imshow('binary', binary)
            if image_name == "Eye_0":
                ag = push_val(total_white)
                # print image_name, " : ", total_white, " : ", ag

            # print "Black ", total_black
            # print "White ", total_white

            if (simulate_real_time == "true"):
                pass
                # put number on image
                if (cnt_eye == 0):
                    cv2.putText(img, "" + str(total_white), (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
                else:
                    cv2.putText(img, "" + str(total_white), (520, 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
                cv2.putText(img, "" + str(threshold), (10, 240), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0))
            else:
                # Plot Histogram
                plt.subplot(2, 3, ((cnt_eye * 3) + 1)), plt.hist(roi_eye_gray.ravel(), 256, [0, 256])
                plt.title(image_name + ' Hist')
                # Plot Eye Images
                plt.subplot(2, 3, ((cnt_eye * 3) + 2)), plt.imshow(roi_eye_color, 'gray')
                plt.title(image_name + ' Image Threshold')

                # Plot Eye Images after threshold
                plt.subplot(2, 3, ((cnt_eye * 3) + 3)), plt.imshow(roi_eye_gray2, 'gray')
                plt.title(image_name + ' Image')

            cnt_eye = cnt_eye + 1
        if len(eyes) == 0:
            ag = push_val(0)

        # Decision Making
        average = avg_eyeq()
        if average > 30:

            print
            ("Eye_X: ", average)
            # player.pause()
        else:
            print
            ("---------------------", average)
            winsound.Beep(1000, 100)
    #            pygame.mixer.music.play()
    # if player.playing == False:
    #    print "Play music"
    #    player.queue(music)
    #    player.play()

    # time.sleep(0.5)
    cv2.imshow('frame', img)
    if (simulate_real_time == "false"):
        plt.show()
    # img.releaseImage()
''''''
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(_('Your post is now live!'))
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home Page', form=form, posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)
@app.route('/kaishi')
@login_required

def kaishi():
    flash('您已停止学习')
    if (simulate_real_time == "true"):
        global cap,frame,istrue,T1,T2
        T1 = time.time()
        istrue=1
        cap = cv2.VideoCapture(0)
        countQuit = 10
        k = 0
        while (istrue==1):
            # time.sleep(1)
            ret, frame = cap.read()
            if frame.any() != None:
                # frame = cv2.resize(frame, (600, 350))
                cv2.imshow('frame', frame)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                detect_and_draw(frame, gray)
                if cv2.waitKey(1) & 0xFF == ord('q') or istrue==0:
                    T2 = time.time()
                    flash('您的学习时间为'+str(int(T2-T1))+'秒')
                    cap.release()
                    cv2.destroyAllWindows()
                    return redirect(url_for('login'))
            else:
                print("Frame Grabbed Problem")
                countQuit = countQuit - 1
                if countQuit <= 0:
                    break
                else:
                    continue
    else:
        # Capture frame-by-frame
        frame = cv2.imread('face_img.jpg')

        # Resize Image
        frame = cv2.resize(frame, (600, 350))

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.waitKey(1)
        detect_and_draw(frame, gray)
        cv2.waitKey(0)

        # Display the resulting frame
        #cv2.imshow('frame',gray)
        return redirect(url_for('login'))

@app.route('/guanbi')
@login_required
def guanbi():
    istrue=0
    flash('您已停止学习')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])  # 既支持注册，又支持登录
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # 重定向到 next 页面
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('恭喜！你现在有了一个在伴你学上的新账户！'))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('邮件已发送，请根据发送的邮件重置你的密码')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('你的密码已经重置'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body':'Test post #1'},
        {'author':user, 'body':'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash(_('你的更改已保存.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('用户{} 没有找到.'.format(username))
        return redirect(url_for('index'))
    if user== current_user:
        flash(_('你不能关注你自已'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('你已经关注了{}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash('用户{} 没有找到.'.format(username))
        return redirect(url_for('index'))
    if user== current_user:
        flash(_('你不能关注你自已!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('你已经取消关注{}!'.format(username))
    return redirect(url_for('user', username=username))


