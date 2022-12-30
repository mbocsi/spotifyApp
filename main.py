from freshplaylist import FreshPlaylist
from topplaylist import TopPlaylist
from job import JobInterface
import os

CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']


class App:
    def __init__(self, jobs: list) -> None:
        self.jobs = jobs

    def __init__(self) -> None:
        self.jobs = []

    def run(self) -> None:
        for job in self.jobs:
            job.run()

    def add_job(self, job: JobInterface) -> None:
        self.jobs.append(job)


if __name__ == '__main__':
    app = App()
    app.add_job(FreshPlaylist('F1ux', 'F1ux Fresh - Scripted', 30))
    app.add_job(TopPlaylist(playlist='Top 50 - Scripted', limit=50))
    app.add_job(TopPlaylist(playlist='Top 25 - Scripted', limit=25))
    app.run()
