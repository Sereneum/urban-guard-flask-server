from models import init_event_model
from datetime import datetime


class DatabaseService:
    def __init__(self, db, ftp_service):
        self.db = db
        self.ftp_service = ftp_service
        self._event_model = init_event_model(db)
        print({"event_model": self._event_model})

    def add_event(self, form, file):
        new_event = self._event_model(
            camera_id=int(form['camera_id']),
            event_timestamp=datetime.strptime(form['event_timestamp'], "%Y-%m-%d %H:%M:%S"),
            event_type=form['event_type'],
            event_name=form['event_name'],
            event_image=form['event_image'],
            coordinates=form['coordinates'],
            address=form['address'],
            event_state=int(form['event_state'])
        )
        self.db.session.add(new_event)
        self.db.session.commit()
        self.ftp_service.save_file(file=file, file_index=new_event.event_id)

    def get_all(self):
        all_events = self._event_model.query.all()

        events_data = [
            {
                'event_id': event.event_id,
                'camera_id': event.camera_id,
                'event_timestamp': event.event_timestamp,
                'event_type': event.event_type,
                'event_name': event.event_name,
                'event_image': event.event_image,
                'coordinates': event.coordinates,
                'address': event.address,
                'event_state': event.event_state
            }
            for event in all_events
        ]

        return events_data



