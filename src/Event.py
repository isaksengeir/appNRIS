from src.static_methods import event_body
from datetime import date


class Attendee:
    def __init__(self, email="None", responseStatus="needsAction", attendee=None):

        self._id = None # The attendee's Profile ID, if available.
        self._email = email
        self._displayName = None #The attendee's name, if available
        self._organizer = False # Whether the attendee is the organizer of the event
        self._optional = False # Whether this is an optional attendee ? bool
        self._comment = None # The attendee's response comment.
        self._responseStatus = responseStatus

        if attendee:
            for k, v in attendee.items():
                setattr(self, k, v)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" in value:
            self._email = value

    @property
    def responseStatus(self):
        return self._responseStatus

    @responseStatus.setter
    def responseStatus(self, value):
        self._responseStatus = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, value):
        if isinstance(value, bool):
            self._optional = value

    @property
    def organizer(self):
        return self._organizer

    @organizer.setter
    def organizer(self, value):
        if isinstance(value, bool):
            self._organizer = value

    @property
    def displayName(self):
        return self._displayName

    @displayName.setter
    def displayName(self, value):
        self._displayName = value

    @property
    def body(self):
        # keywords & properties keeping things compact:
        keycontent = {"id": self.id, "email": self.email, "displayName": self.displayName,
                           "organizer": self.organizer, "optional": self.optional, "comment": self.comment,
                           "responseStatus": self._responseStatus}
        body = dict()
        for k in keycontent.keys():
            if keycontent[k]:
                body[k] = keycontent[k]
        return body


class Attendees:
    def __init__(self, attendees):
        self._all = [Attendee(attendee=i) for i in attendees]
        self._attendee = self.all[-1]

    @property
    def all(self):
        return self._all

    @property
    def attendees_body(self):
        return [attendee.body for attendee in self._all]

    @property
    def attendee(self):
        return self._attendee

    @attendee.setter
    def attendee(self, value):
        if value not in self.all:
            if isinstance(value, dict):
                if "email" in value.keys():
                    self._all.append(Attendee(attendee=value))
            elif isinstance(value, Attendee):
                self._all.append(value)
            else:
                return
            self._attendee = self._all[-1]
        elif value in self._all:
            self._attendee = value
            return
        elif isinstance(value, str) and "@" in value:
            self.set_current_attendee(value)

    def set_current_attendee(self, email):
        for who in self._all:
            if who.email == email:
                self._attendee = who

    @attendee.deleter
    def attendee(self):
        del self._all[self._all.index(self._attendee)]
        try:
            self._attendee = self._all[0]
        except IndexError:
            self._all = None


class Event:
    def __init__(self, event):
        self._id = None
        self._created = ""
        self._start = ""
        self._end = ""
        self._summary = ""
        self._location = ""
        self._description = ""
        self._attendees = None
        self._timezone = "Europe/Oslo"

        #self.keyproperty = {"id": self._id, "created": self._created, "summary": self._summary,
        #                    "location": self._location,
        #                    "description": self._description}

        if event:
            self._body = event
        else:
            self._body = event_body()

        self.read_event()

    def read_event(self):
        for k, v in self.body.items():
            try:
                setattr(self, k, v)
            except AttributeError:
                print(f"Attribute problems with: {k}")
                pass

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def attendees(self):
        return self._attendees

    @attendees.setter
    def attendees(self, value):
        if isinstance(value, Attendees):
            self._attendees = value
        else:
            self._attendees = Attendees(attendees=value)

    @property
    def body(self):
        if self.attendees:
            self._body["attendees"] = self.attendees.attendees_body

        return self._body

    @body.setter
    def body(self, value):
        if isinstance(value, dict):
            self._body.update(value)
        else:
            print("body property takes dict...")
            print(value)

    @property
    def start(self):
        """
        Typical format: 2021-09-14T09:22:26.000Z
        """
        return self._start

    @start.setter
    def start(self, value):
        if isinstance(value, dict):
            self._start = value.get("date")
        else:
            self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if isinstance(value, dict):
            self._end = value.get("date")
        else:
            self._end = value

    @property
    def start_week(self):
        return date(*map(int, self.start.split("T")[0].split("-")[0:3])).isocalendar()[1]

    @property
    def end_week(self):
        return date(*map(int, self.end.split("T")[0].split("-")[0:3])).isocalendar()[1]

    @property
    def start_year(self):
        return self.start.split("-")[0]

    @property
    def end_year(self):
        return self.end.split("-")[0]

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value
        self.body = {"summary": value}


class RT_Event(Event):
    def __init__(self, event, institution=None):
        self._ukevakt = False
        self._institution = institution

        super(RT_Event, self).__init__(event)

    def check_ukevakt(self):
        if "ukevakt" in self.summary.lower():
            self.ukevakt = True

    def guess_instituion(self):
        if ":" in self.summary:
            self._institution = self.summary.split(":")[0].split("(")[0].strip()

    @property
    def institution(self):
        return self._institution

    @institution.setter
    def institution(self, value):
        self._institution = value

    @property
    def ukevakt(self):
        return self._ukevakt

    @ukevakt.setter
    def ukevakt(self, value):
        if isinstance(value, bool):
            self._ukevakt = value

    @property
    def summary(self):
        if self._institution:
            if self._institution not in self._summary:
                self._summary = f"{self._institution}: {self._summary}"
        if self._ukevakt and "ukevakt" not in self._summary.lower():
            self._summary = f"{self._summary} (ukevakt)"
        if not self._ukevakt and "ukevakt" in self._summary.lower():
            self._summary = self._summary.split("(")[0].strip()

        return self._summary

    @summary.setter
    def summary(self, value):
        print("I got this value for summary setter:")
        print(value)

        if "ukevakt" in value.lower():
            self.ukevakt = True
        else:
            if self.ukevakt:
                value += " (ukevakt)"
        if ":" in value:
            if self._institution:
                if self._institution not in value:
                    wtf = value.split(":")[0].split("(")[0].strip()
                    value = value.replace(wtf, self._institution)
                    print(f"I will not allow you to change from f{self._institution} to {wtf}")
            else:
                self._institution = value.split(":")[0].split("(")[0].strip()
        else:
            if self.institution:
                value = f"{self.institution}:{value}"
        self._summary = value
        self.body = {"summary": f"{value}"}

    @property
    def summary_names(self):
        return self.summary.split(":")[-1].replace("(Ukevakt)", "").replace("(ukevakt)", "")


    @property
    def summary_names_ukevakt(self):
        return self.summary.split(":")[-1]




