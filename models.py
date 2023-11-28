def init_event_model(db):
    class Event(db.Model):
        __tablename__ = 'Event'

        event_id = db.Column(db.Integer, primary_key=True)
        camera_id = db.Column(db.Integer)
        event_timestamp = db.Column(db.DateTime)
        event_type = db.Column(db.String)
        event_name = db.Column(db.String)
        event_image = db.Column(db.String)
        coordinates = db.Column(db.String)
        address = db.Column(db.String)
        event_state = db.Column(db.Integer)

    return Event
