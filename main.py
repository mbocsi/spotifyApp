from freshplaylist import FreshPlaylist
from topplaylist import TopPlaylist
from job import JobInterface
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ['SPOTIPY_CLIENT_ID']
CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
REDIRECT_URI = os.environ['SPOTIPY_REDIRECT_URI']


class App:
    def __init__(self, jobs: list = []):
        """
        :param jobs: A queue of jobs that will be executed on run()
        """
        self.jobs = jobs

    def run(self):
        """
        Runs all the jobs in the queue
        """
        for job in self.jobs:
            job.run()

    def add_job(self, job: JobInterface):
        """
        Adds a job to the queue
        :param job: The Job that is added
        """
        self.jobs.append(job)


def main():
    app = App()

    # Create a playlist called 'F1ux Fresh - Scripted' that contains songs from 'F1ux' added in the last 30 days
    app.add_job(FreshPlaylist('F1ux', 'F1ux Fresh - Scripted', 30))

    # Create playlists for my top 25 and 50 songs
    app.add_job(TopPlaylist(playlist='Top 50 - Scripted', limit=50))
    app.add_job(TopPlaylist(playlist='Top 25 - Scripted', limit=25))

    # Run the scripts
    app.run()

if __name__ == '__main__':
    main()
