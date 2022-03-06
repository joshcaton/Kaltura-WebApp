from flask import Flask, render_template, request, flash

from KalturaClient import *
from KalturaClient.Plugins.Core import *

app = Flask(__name__)
app.DEBUG = True
app.secret_key = "K_J_T"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/")
def index():
	config = KalturaConfiguration(4530233)
	config.serviceUrl = "https://www.kaltura.com/"
	client = KalturaClient(config)
	print("KalturaClient object instantiated")

	secret = "fe3397b78566adecf8de92e4ae747d3d"
	user_id = "joshcaton@live.com"
	k_type = KalturaSessionType.ADMIN
	partner_id = "4530233"
	expiry = 86400
	privileges = ""

	ks = client.session.start(secret, user_id, k_type, partner_id, expiry, privileges)
	client.setKs(ks)

	print("KalturaClient connection started")
	filter = KalturaCategoryEntryFilter()
	filter.categoryIdIn = "250036913, 250036923"
	pager = KalturaFilterPager()

	result = client.categoryEntry.list(filter, pager)
	print(result)

	entries = []
	for x in range(len(result.objects)):
	    entries.append( result.objects[x].entryId)

	flash("Please select a video from the list of Entity IDs")
	option_list = result.objects

	return render_template("index.html", option_list=entries, route="index")

@app.route("/bonus", methods=['POST', 'GET'])
def greeter():
	flash("Loaded your previous selection: " + str(request.form['option']))
	return render_template("playerCSS.html", e_id=str(request.form['option']))
