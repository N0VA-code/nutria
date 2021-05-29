#!/usr/bin/python3
import json
import argparse
import nutria_config
import nutria_crawling
from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response

app = Flask(__name__, template_folder=nutria_config.WEBDIR)

@app.route('/', methods=['POST', 'GET'])
def home():
    meal = []
    userInfo = {
        'height' : '',
        'weight' : ''
            }
    dishList = []
    if request.cookies.get('dishList') != None:
        dishList = json.loads(request.cookies.get('dishList'))
    if request.cookies.get('meal') != None:
        meal = json.loads(request.cookies.get('meal'))
    if request.cookies.get('userInfo') != None:
        userInfo = json.loads(request.cookies.get('userInfo'))
    if request.method == 'POST':
        if 'weight' and 'height' in request.form:
            userInfo['height'] = request.form['height']
            userInfo['weight'] = request.form['weight']
        elif 'dish' in request.form:
            dishData = nutria_crawling.getListOfDish(request.form['dish'])
            dishList = dishData['listOfDish']
        elif 'add' in request.form:
            e = dishList[int(request.form['add'])]
            meal = meal + list([e])
        elif 'delete' in request.form:
            for e in meal:
                if str(e['url']) == str(request.form['delete']):
                    meal.remove(e)
                    break

        resp = make_response(render_template('index.html', meal=meal, dishList=dishList, userInfo=userInfo))
        resp.set_cookie('meal', json.dumps(meal))
        resp.set_cookie('dishList', json.dumps(dishList))
        resp.set_cookie('userInfo', json.dumps(userInfo))
    else: # GET
        resp = render_template('index.html', meal=meal, dishList=dishList, userInfo=userInfo)
    return resp

@app.route('/login') # TBD - login or load
def login():
    return ''

@app.route('/results')
def results():
    # results test
    return request.cookies

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
