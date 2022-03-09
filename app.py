from flask import Flask, render_template, Response, jsonify, url_for
import gunicorn
import os
from camera import *

app = Flask(__name__)
picFolder = os.path.join('static','emojis')
app.config['UPLOAD_FOLDER'] = picFolder

@app.route("/")
def index():
    return render_template("index.html")

headings = ("Name","Album","Artist")
df1 = music_rec()
df1 = df1.head(15)
@app.route('/next')
def next():
    print(df1.to_json(orient='records'))
    angry = os.path.join(app.config['UPLOAD_FOLDER'],'image1.jpg')
    return render_template('next.html', headings=headings, data=df1,user_image = angry)

def gen(camera):
    while True:
        global df1
        frame, df1 = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


#@app.route('/emoji')
#def emoji():
#    return "heloo,world"

@app.route('/t')
def gen_table():
    return df1.to_json(orient='records')



if __name__ == '__main__':
    app.debug = True
    app.run()
