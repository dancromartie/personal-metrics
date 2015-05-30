from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import re

app = Flask(__name__)
app.config["DEBUG"] = True

METRICS_PATH = "metrics.json"
CONFIG_PATH = "config/key_config.json"

@app.route("/metrics_app")
def hello():
    return render_template("metrics_interface.html")

@app.route("/dump_metrics")
def dump_metrics():
    metrics_text = json.dumps(get_metrics_dict())
    return metrics_text

@app.route("/dump_config")
def dump_config():
    config_dict = json.loads(open(CONFIG_PATH, "r").read())
    config_dict["time_info"] = {}
    config_dict["time_info"]["now"] = str(datetime.now())
    return json.dumps(config_dict)

def get_metrics_dict():
    metrics_text = open(METRICS_PATH, "r").read()
    metrics_dict = json.loads(metrics_text)
    return metrics_dict

def write_metrics_dict(dict_to_write):
    open(METRICS_PATH, "w").write(json.dumps(dict_to_write))


@app.route("/add_key", methods=["POST", "GET"])
def add_key():
    key_name = request.form["key_to_add"].strip()
    if key_name != "":
	metrics_dict = get_metrics_dict()
	metrics_dict[key_name] = {}
	write_metrics_dict(metrics_dict)
    return redirect(url_for("hello"))

@app.route("/remove_key", methods=["POST", "GET"])
def remove_key():
    key_name = request.form["key_to_remove"].strip()
    if key_name != "":
	metrics_dict = get_metrics_dict()
	metrics_dict.pop(key_name, None)
	write_metrics_dict(metrics_dict)
    return redirect(url_for("hello"))

@app.route("/store_metrics", methods=["POST", "GET"])
def store_metrics():
    metrics_as_dict = get_metrics_dict()
    todays_iso_date = datetime.now().isoformat()[0:10]
    date_override = request.form["date_override"]
    if date_override != "":
	    if re.match(r"^\d\d\d\d-\d\d-\d\d$", date_override):
		todays_iso_date = date_override
	    else:
		return "woops!  bad processing of date override"
    for key in request.form:
	if key == "date_override":
	    continue
	print key
	val = request.form[key]
	if val.strip() == "":
	    continue
	else:
	   val = float(val.strip())
	metrics_as_dict[key][todays_iso_date] = val
    write_metrics_dict(metrics_as_dict)
    return redirect(url_for("hello"))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
	
