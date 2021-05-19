#!/usr/bin/python3
import argparse
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return ''

@app.route('/load') # TBD - login or load
def load():
    return ''

@app.route('/results')
def results():
    return ''

@app.route('/credit')
def credit():
    return ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="") 
    parser.add_argument('--listen-port', type=str, required=False, default='5000', help='REST service listen port')
    parser.add_argument('--listen-addr', type=str, required=False, default='127.0.0.1', help='REST service listen addr')
    args = parser.parse_args() 
    listen_port = args.listen_port
    listen_addr = args.listen_addr

    print("Starting the service with ip_addr="+listen_addr)
    app.run(debug=False,host=listen_addr,port=int(listen_port))
