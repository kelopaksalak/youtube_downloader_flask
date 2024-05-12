from flask import Flask, request, render_template, redirect, url_for, flash, session
from pytube import YouTube, extract
from pytube.exceptions import RegexMatchError, VideoUnavailable, AgeRestrictedError
from path import choose_file_path_audio, choose_file_path_video
import os

app = Flask(__name__)
app.config['SESSION_PERMENANT'] = False
app.secret_key = "12345"

@app.route('/', methods=['GET', 'POST'])
def index():
    choose_path = ''
    if request.method == 'POST':
        youtube_url = request.form['link-yt']
        session['path_format'] = request.form['format']
        yt_id = extract.video_id(youtube_url)
        try:
            yt = YouTube(youtube_url)
            session['filename'] = yt.streams[0].title
            youtube_format = int(session.get('path_format', None))
            video_path = choose_file_path_video()
            audio_path = choose_file_path_audio()
            if youtube_format == 1:
                streams = yt.streams.filter(progressive=True, file_extension="mp4")
                highest_res_stream = streams.get_highest_resolution()
                highest_res_stream.download(output_path=video_path)
            else:
                streams = yt.streams.filter(only_audio=True)
                streams[0].download(output_path=audio_path)
            return redirect(url_for('successful', yt_id=yt_id))
        except RegexMatchError:
            flash("Invalid YouTube URL.")
        except AgeRestrictedError:
            flash("This video is age-restricted.")
        except VideoUnavailable:
            flash("The video is not available.")
        except Exception as e:
            flash("Oops something went wrong!")
    return render_template('index.html')

@app.route('/successful/<yt_id>')
def successful(yt_id):
    path_format = int(session.get('path_format', None))
    filename = str(session.get('filename', None))
    print(f'Youtube video ID : {yt_id}')
    if path_format == 1:
        path_download = choose_file_path_video()
    else:
        path_download = choose_file_path_audio()
    return render_template('successful.html', path_file=path_download, filename =filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
