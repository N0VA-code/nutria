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
    dishData = []
    currentPage = 0
    if request.cookies.get('meal') != None:
        meal = json.loads(request.cookies.get('meal'))
    if request.cookies.get('userInfo') != None:
        userInfo = json.loads(request.cookies.get('userInfo'))
    if request.cookies.get('dishData') != None:
        dishData = json.loads(request.cookies.get('dishData'))
    if request.cookies.get('currentPage') != None:
        currentPage = json.loads(request.cookies.get('currentPage'))
    if request.method == 'POST':
        if request.cookies.get('dishData') != None and 'page' in request.form:
            currentPage = min(int(request.form['page']), int(dishData['pages'])-1)
            dishData = nutria_crawling.getListOfDish(dishData['keyword'], currentPage)
        elif 'weight' and 'height' in request.form:
            userInfo['height'] = request.form['height']
            userInfo['weight'] = request.form['weight']
        elif 'dish' in request.form:
            currentPage = 0
            dishData = nutria_crawling.getListOfDish(request.form['dish'], currentPage)
        elif 'add' in request.form:
            e = dishData['listOfDish'][int(request.form['add'])]
            meal = meal + list([e])
        elif 'delete' in request.form:
            for e in meal:
                if str(e['url']) == str(request.form['delete']):
                    meal.remove(e)
                    break
        resp = make_response(render_template('index.html', meal=meal, dishData=dishData, userInfo=userInfo, currentPage=currentPage))
        resp.set_cookie('currentPage', json.dumps(currentPage))
        resp.set_cookie('meal', json.dumps(meal))
        resp.set_cookie('dishData', json.dumps(dishData))
        resp.set_cookie('userInfo', json.dumps(userInfo))
    else: # GET
        resp = render_template('index.html', meal=meal, dishData=dishData, userInfo=userInfo, currentPage=currentPage)
    return resp

@app.route('/login') # TBD - login or load
def login():
    return ''

@app.route('/results')
def results():
    # results test
    meal = json.loads(request.cookies.get('meal'))
    userInfo = json.loads(request.cookies.get('userInfo'))
    test = ''
    test += str(userInfo)
    for dish in meal:
        test += str(nutria_crawling.getNutrientInfoFromDish(dish)) + '\n'
    return test

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
