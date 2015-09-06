import argparse
from flask import Flask, send_from_directory
from flask import request
import os

app = Flask(__name__)

garageTaken = False

@app.route("/")
def showStatus():
    if garageTaken == True:
        # show picture, whatever..
        #return "Garage is taken..."
    	return send_from_directory(app.config['IMAGE_FOLDER'], 'taken.jpg', add_etags=False)
    else:
        #show other picture..
        #return "Garage is not taken.."
	return send_from_directory(app.config['IMAGE_FOLDER'], 'empty.jpg', add_etags=False)


@app.route('/data')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    user = request.args.get('user')
    return "User: " + user

# updates garageStatus
@app.route('/input')
def updateStatus():
    global garageTaken
    taken = request.args.get('garageStatus')
    if taken == '1':
        garageTaken = True
    else:
        garageTaken = False
    return "Set garage to taken" if garageTaken else "Set garage to free"
    
# Parse arguments from CLI
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', action='store', default="0.0.0.0")
#parser.add_argument('--host', dest='host', action='store', default="192.168.0.102")
    parser.add_argument('-d','--debug', dest='debug', action='store_true', default=False)
    parser.add_argument('-p','--port', dest='port', action='store', type=int, default=80)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    app.debug = args.debug

    app_dir = os.path.dirname(os.path.abspath(__file__))
    app.config['IMAGE_FOLDER'] = os.path.join(app_dir + '/img')

    app.run(host = args.host, port = args.port)

