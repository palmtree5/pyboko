from datetime import datetime
from typing import List


BOKO_API_URL = "https://api.bokoblin.com"


class Marathon:
    def __init__(self, data):
        self.id = int(data.get("id", None))
        self.type = data.get("type", None)
        self.type_id = data.get("type_id", None)
        self.slug = data.get("slug", None)
        self.full_name = data.get("full_name", None)
        self.total = data.get("total", None)
        sd = data.get("start_date", None)
        if sd:
            self.start_date = datetime.strptime(sd, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.start_date = sd
        ed = data.get("stop_date", None)
        if ed:
            self.stop_date = datetime.strptime(ed, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.stop_date = ed
        self.playlist = data.get("playlist", None)
        self.charity = Charity(data.get("charity", None))
        self.segments = [Segment(segment) for segment in data.get("segments", [])]
        self.attendance = [Attendance(attendee) for attendee in data.get("attendance", [])]
    
    async def get_attendees(self, _session):
        """
        Gets a list of attendees for the marathon
        """
        body = """
        query($marathon_id: Int!){
            marathon(id: $marathon_id){
                attendance{
                    location
                    attendee{
                        id
                        name
                        twitch_login
                        rank
                        house
                        house_color
                    }
                }
            }
        }"""
        headers = {"Content-Type": "application/json"}
        async with _session.post(url=BOKO_API_URL, headers=headers, json={"query": body, "variables": {"marathon_id": int(self.id)}}) as resp:
            data = await resp.json()
        self.attendance = [Attendance(attendee) for attendee in data["data"]["marathon"]["attendance"]]

    async def get_segments(self, _session):
        """
        Gets a list of segments that occurred during the marathon
        """
        body = """
        query($marathon_id: Int!){
            marathon(id: $marathon_id){
                segments{
                    id
                    game{
                        id
                        title
                        isZelda
                        isEvent
                    }
                    modifier
                    raised
                    start_time
                    end_time
                    vod
                    time_offset
                    runners{
                        attendee{
                            id
                            name
                            twitch_login
                            rank
                        }
                        runner_rank
                    }
                    filenames{
                        filename
                        note
                    }
                }
            }
        }"""
        headers = {"Content-Type": "application/json"}
        async with _session.post(url=BOKO_API_URL, headers=headers, json={"query": body, "variables": {"marathon_id": int(self.id)}}) as resp:
            data = await resp.json()
        self.segments = [Segment(segment) for segment in data["data"]["marathon"]["segments"]]


class Segment:
    def __init__(self, data):
        self.id = data.get("id", None)
        mar = data.get("marathon", None)
        if mar:
            self.marathon = Marathon(mar)
        else:
            self.marathon = None
        self.game = Game(data.get("game", None))
        self.modifier = data.get("modifier", None)
        self.raised = data.get("raised", None)
        sd = data.get("start_time", None)
        if sd:
            self.start_time = datetime.strptime(sd, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.start_time = sd
        ed = data.get("end_time", None)
        if ed:
            self.end_time = datetime.strptime(ed, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.end_time = ed
        self.vod = data.get("vod", None)
        self.time_offset = data.get("time_offset", None)
        self.runners = [Runner(runner) for runner in data.get("runners")]
        self.filenames = [Filename(filename) for filename in data.get("filenames")]


class Runner:
    def __init__(self, data):
        self.attendee = Attendee(data.get("attendee", None))
        self.runner_rank = data.get("runner_rank", None)


class Filename:
    def __init__(self, data):
        self.segment_id = data.get("segment_id", None)
        self.filename = data.get("filename", None)
        self.note = data.get("note", None)


class Game:
    def __init__(self, data):
        self.id = data.get("id", None)
        self.title = data.get("title", None)
        self.segments = [Segment(segment) for segment in data.get("segments", [])]
        self.isZelda = data.get("isZelda", None)
        self.isEvent = data.get("isEvent", None)


class Charity:
    def __init__(self, data):
        self.id = data.get("id", None)
        self.slug = data.get("slug", None)
        self.full_name = data.get("full_name", None)
        self.website = data.get("website", None)
        self.total = float(data.get("total", None))


class Attendance:
    def __init__(self, data):
        self.id = data.get("id", None)
        att = data.get("attendee", None)
        if att:
            self.attendee = Attendee(att)
        else:
            self.attendee = None
        mar = data.get("marathon", None)
        if mar:
            self.marathon = Marathon(mar)
        else:
            self.marathon = None

        self.award = data.get("award", None)
        self.location = data.get("location", None)


class Attendee:
    def __init__(self, data):
        self.id = data.get("id", None)
        self.name = data.get("name", None)
        self.twitch_login = data.get("twitch_login", None)
        self.rank = data.get("rank", None)
        self.house = data.get("house", None)
        self.house_color = data.get("house_color", None)