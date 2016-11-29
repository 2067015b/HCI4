from bottle import *
from dbmanager import DBManager


@route('/submit-bulb-datapoint')
def submit_bulb_datapoint():
    '''Submits a point  for the bulbName into the db. '''
    bulb_name = request.query['bulbName']
    db = DBManager()

    user_data = db.get("USER")
    user_data[bulb_name][request.query['state']]+=1
    db.save("USER",user_data)

    # This gets returned to whoever made the request (so if you load the URL from a browser you'll see this response)
    return "The data has been added to the aggregate in the pickle for bulb %s: state number: %s" % (bulb_name, str(request.query['state']))


@route('/wipe-all-aggregated-data')
def wipe_all_aggregated_data():
    return DBManager().reset()

@route('/get-stats')
def get_stats():

    bulb_name = request.query['bulbName']
    db = DBManager()
    user_data = db.get("USER")

    return user_data[bulb_name]




# This actually spins up the server and it starts listening. To listen on 0.0.0.0 you might need root privileges
run(host='0.0.0.0', port=8555, debug=True)
