#!/usr/bin/python3
import json
import argparse
import nutria_config
from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response

app = Flask(__name__, template_folder=nutria_config.WEBDIR)

@app.route('/', methods=['POST', 'GET'])
def home():
    meal = ''
    if request.method == 'POST':
        if request.cookies.get('meal') != None:
            meal = json.loads(request.cookies.get('meal')) + list([request.form['dish']])
        else:
            meal = list([request.form['dish']])
        resp = make_response(render_template('index.html', meal=meal))
        resp.set_cookie('meal', json.dumps(meal))
    else:
        if request.cookies.get('meal') != None:
            meal = json.loads(request.cookies.get('meal'))
        resp = render_template('index.html', meal=meal)
    return resp

@app.route('/login') # TBD - login or load
def load():
    return ''

@app.route('/results', methods=['POST'])
def results():
    # print results
    return ''

@app.route('/credit')
def credit():
    return render_template('credit.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="") 
    parser.add_argument('--listen-port', type=str, required=False, default=nutria_config.WEB_PORT, help='REST service listen port')
    parser.add_argument('--listen-addr', type=str, required=False, default=nutria_config.HOST, help='REST service listen addr')
    args = parser.parse_args() 
    listen_port = args.listen_port
    listen_addr = args.listen_addr

    print("Starting the service with ip_addr="+listen_addr)
    app.run(debug=False,host=listen_addr,port=int(listen_port))
