from spotify_scripts.freshplaylist import FreshPlaylist
from spotify_scripts.topplaylist import TopPlaylist
from spotify_scripts.job import JobInterface
from dotenv import load_dotenv
import argparse
import json

load_dotenv()

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
    # Parse in the CLAs (config file)
    parser = argparse.ArgumentParser(prog="spotify_scripts",
                                     description="creates spotify playlists")
    
    parser.add_argument('config', type=str, help="path to the config file containing script jobs")
    args = parser.parse_args()
    config_path = args.config

    with open(config_path, 'r') as f:
        content = f.read()
    
    jobs = json.loads(content)

    # Create the script runner
    app = App()

    # Add the jobs that create fresh playlists
    if "fresh_playlists" in jobs:
        for fresh_job in jobs["fresh_playlists"]:
            original_playlist = fresh_job["original_playlist"]
            fresh_playlist = fresh_job["fresh_playlist"]
            duration = fresh_job["duration"]
            app.add_job(FreshPlaylist(original_playlist=original_playlist,
                                       fresh_playlist=fresh_playlist, 
                                       duration=duration))
    
    # Add the jobs that create top playlists
    if "top_playlists" in jobs:
        for top_job in jobs["top_playlists"]:
            playlist = top_job["playlist_name"]
            limit = top_job["limit"]
            app.add_job(TopPlaylist(playlist=playlist, limit=limit))

    # Run the scripts
    app.run()

if __name__ == '__main__':
    main()
