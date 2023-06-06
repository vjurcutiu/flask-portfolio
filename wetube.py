import functools
import os
from wetube_api_call import wetube_api_call
from wetube_api_call2 import wetube_api_call2
from wac import wac

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash
import os
from portfolio.db import get_db

bp = Blueprint('wetube', __name__, url_prefix='/wetube')

@bp.route('')
def redirect_home():
    return redirect(url_for('wetube.home', page=0))

@bp.route('/<page>')
def home(page):
    video_data = wac.home_page()     
    videos =[]
    titles= []
    video = {}
    tooltips = []
    for i in range(50):
        if len(video_data['items'][i]['snippet']['title']) >= 50:
            vid = video_data['items'][i]['snippet']['title'][0:47] + '...'
            titles.append(vid.replace('&amp;','&').replace('&#39;', '\''))
        else:
            titles.append(video_data['items'][i]['snippet']['title'].replace('&amp;','&').replace('&#39;', '\''))
        tooltips.append(video_data['items'][i]['snippet']['title'].replace('&amp;','&').replace('&#39;', '\''))
    for n in range(50):   
        try:   
            video = {'id': video_data['items'][n]['id'],
                    'titles' : titles[n],
                    'descriptions' :video_data['items'][n]['snippet']['description'],
                    'thumbnails' : video_data['items'][n]['snippet']['thumbnails']['medium']['url'],
                    'tooltips': tooltips[n]
                    }
            videos.append(video)
        except:
            continue

    return render_template('wetube_home.html', videos = videos, page=page)
    

@bp.route('/search', methods=['POST', 'GET'])
def search():    
    search_term = request.form.get('search-term')
    video_data = wac.search(search_term)      
    videos =[]
    titles= []
    video = {}
    tooltips = []
    for i in range(25):
        if len(video_data['items'][i]['snippet']['title']) >= 50:
            vid = video_data['items'][i]['snippet']['title'][0:47] + '...'
            titles.append(vid.replace('&amp;','&').replace('&#39;', '\''))
        else:
            titles.append(video_data['items'][i]['snippet']['title'].replace('&amp;','&').replace('&#39;', '\''))
        tooltips.append(video_data['items'][i]['snippet']['title'].replace('&amp;','&').replace('&#39;', '\''))
    for n in range(25):
        try:     
            video = {'id': video_data['items'][n]['id']['videoId'],
                    'titles' : titles[n],
                    'descriptions' :video_data['items'][n]['snippet']['description'],
                    'thumbnails' : video_data['items'][n]['snippet']['thumbnails']['medium']['url'],
                    'tooltips': tooltips[n],
                    'uploader': video_data['items'][n]['snippet']['channelTitle']
                    }
            videos.append(video)
        except:
            continue
    return render_template('wetube_search.html', videos = videos, search_term=search_term)

@bp.route('/videos/<id>', methods = ['GET'])
def videos(id):    
    related_vids = wac.related_vids(id)
    rel_vids = []
    for n in range(len(related_vids)):
        try:
            related_vid = {'id': related_vids['items'][n]['id']['videoId'],
                            'title': related_vids['items'][n]['snippet']['title'],
                            'thumbnail': related_vids['items'][n]['snippet']['thumbnails']['medium']['url']
                            }
            rel_vids.append(related_vid)
        except:
            pass
    vid_info = wac.search_by_id(id)
    vid_info = {
        'title' : vid_info['items'][0]['snippet']['title'],
        'description' : vid_info['items'][0]['snippet']['description'],
        'uploader' : vid_info['items'][0]['snippet']['channelTitle']
    }
    return render_template('videos.html', id = id, rel_vids = rel_vids, vid_info = vid_info)
    
@bp.route('/login', methods=['POST', 'GET'])
def login():   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('wetube.home'))

        flash(error)

    return render_template('login.html')

@bp.route('/signup', methods=['POST', 'GET'])
def signup():   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("wetube.login"))

        flash(error)

    return render_template('signup.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('wetube.home'))

@bp.route('/save_video/<id>', methods=['GET'])
def save_video(id):
    error = None
    if error is not None:
            flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO video (video, username_id)'
            ' VALUES (?, ?)',
            (id, g.user['id'])
        )
        db.commit()
        return redirect('/wetube/saved_videos')    
    return render_template('videos.html', id = id) 

@bp.route('/remove_video/<id>', methods=['GET'])
def remove_video(id):
    
    error = None
    if error is not None:
            flash(error)
    else:
        db = get_db()
        db.execute(
            'DELETE FROM video WHERE video = ?;',
            (id,)
        )
        db.commit()
        return redirect('/wetube/saved_videos')      
    return render_template('videos.html', id = id) 

@bp.route('/saved_videos', methods=['POST','GET'])
def saved_videos():
    db = get_db()
    videos = db.execute(
        'SELECT p.id, video, username_id'
        ' FROM video p JOIN user u ON p.username_id = u.id'
        ' ORDER BY video DESC'
    ).fetchall()    
    video_data_list =[]
    for id in videos:
        video_data = wac.search_by_id(id['video'])
        video_data_list.append(video_data)
    videos_info = []
    titles = []
    tooltips = []
    for i in range(len(video_data_list)):
        if len(video_data_list[i]['items'][0]['snippet']['title']) >= 50:
            vid = video_data_list[i]['items'][0]['snippet']['title'] + '...'
            titles.append(vid.replace('&amp;','&').replace('&#39;', '\''))
        else:
            titles.append(video_data_list[i]['items'][0]['snippet']['title'].replace('&amp;','&').replace('&#39;', '\''))
        tooltips.append(video_data_list[i]['items'][0]['snippet']['title'].replace('&amp;','&').replace('&#39;', '\''))
    for n in range(len(video_data_list)):
        video_info = {'id': video_data_list[n]['items'][0]['id'],
                      'title' : titles[n],
                      'thumbnail': video_data_list[n]['items'][0]['snippet']['thumbnails']['medium']['url'],
                      'tooltips': tooltips[n]
                      }
        videos_info.append(video_info)
    return render_template('saved_videos.html', videos=videos_info, len=len(videos_info))
    

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('wetube.login'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        videos = get_db().execute(
            'SELECT video FROM video WHERE username_id = ?', (user_id,)
        ).fetchall()
        videos = [list(i) for i in videos]
        g.videos = videos