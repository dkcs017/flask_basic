from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField ,validators, ValidationError

class ConfigForm(FlaskForm):
    broker_host = StringField('Broker Host', validators=[validators.input_required()])
    broker_port = IntegerField('Broker Port', validators=[validators.input_required()])

    def validate_broker_port(self, form):
        if self.broker_port.data < 0:
            raise ValidationError('Broker port must be a positive integer.')