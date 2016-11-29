from bottle import *


@route('/submit-bulb-datapoint')
def submit_bulb_datapoint():
    bulb_name = request.query['bulbName']

    submitted_data = {
        "is_on": request.query['isOn'],
        "is_home": request.query['isHome'],
        "is_around": request.query['isAround'],
        "is_in_bed": request.query['isInBed']
    }

    # Debug print statement that would be shown on the server, in the terminal where this runs.
    print "Pretending we actually added the data to the aggregate in the pickle for bulb '%s': %s" % (bulb_name, str(submitted_data))

    # This gets returned to whoever made the request (so if you load the URL from a browser you'll see this response)
    return "Pretending we actually added the data to the aggregate in the pickle for bulb %s: %s" % (bulb_name, str(submitted_data))


@route('/wipe-all-aggregated-data')
def wipe_all_aggregated_data():
    pass

# This actually spins up the server and it starts listening. To listen on 0.0.0.0 you might need root privileges
run(host='0.0.0.0', port=8555, debug=True)
