from __future__ import print_function

from flask import render_template

from flask import Flask, redirect, url_for, flash

from routes import init_api_routes
from routes import init_website_routes

from ConfigForm import ConfigForm
from entity.BrokerConfig import BrokerConfig

import random

# create the Flask application
app = Flask(__name__)

app.secret_key = str(random.randint(1,1000000000))
init_api_routes(app)
init_website_routes(app)


#
# Template filters
#
@app.template_filter('senior_candidate')
def senior_candidate(candidates):
    result = []
    for candidate in candidates:
        for experience in candidate['experience']:
            if experience['years'] >= 5:
                result.append({
                    'first_name': candidate['first_name'],
                    'last_name': candidate['last_name'],
                    'years': experience['years'],
                    'domain': experience['domain']
                })
                break
    return result


configList = []


@app.route('/insertConfig', endpoint='insert_config',methods=['POST','GET'])
def insert_config():
    form = ConfigForm(csrf_enabled=False)
    if form.validate_on_submit():
        record = BrokerConfig(form.broker_host.data,
                     form.broker_port.data)
        configList.append(record)
        flash('Broker config inserted successfully.')
        return redirect(url_for('insert_config'))
    return render_template('config.html', form=form)

if __name__ == "__main__":
    app.run(host='localhost', debug=True)
