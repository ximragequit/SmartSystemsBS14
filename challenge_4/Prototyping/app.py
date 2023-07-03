from flask import Flask, request, render_template, g, current_app, jsonify
import logging
from datetime import datetime
import time

app = Flask(__name__, template_folder='./Templates')

logging.basicConfig(
    format = '______________________\n%(levelname)-2s %(asctime)s \n%(message)s',
    filename = F'.\challenge_4\Prototyping\logs\{datetime.today().strftime("%y.%m.%d")}_flask-app.log', 
    encoding = 'utf-8', 
    level = logging.DEBUG,
    datefmt='%y.%m.%d %H:%M:%S'
    )

def handle_exception(error):
    import traceback
    traceback_str = traceback.format_exc()
    logging.exception(f'An error occurred: {str(error)}')
    return render_template('error.html', error=str(error), traceback = traceback_str), 500

@app.errorhandler(Exception)
def handle_all_exceptions(error):
    return handle_exception(error)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()