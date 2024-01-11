from spotify_scripts.main import App
from spotify_scripts.job import JobInterface
from unittest.mock import patch

def test_init():
    app = App()
    assert app.jobs == []

    app = App([1, 2, 3, 4, 5])
    assert app.jobs == [1, 2, 3, 4, 5]

def test_addjob():
    app = App()
    assert app.jobs == []
    app.add_job(1)
    assert app.jobs == [1]
    app.add_job(2)
    app.add_job(3)
    app.add_job('test')
    assert app.jobs == [1, 2, 3, 'test']

@patch('spotify_scripts.job.JobInterface.run')
def test_run(mock):
    app = App()
    app.run()
    assert mock.call_count == 0
    job = JobInterface()
    app.add_job(job)
    app.run()
    assert mock.call_count == 1
    for _ in range(5): app.add_job(JobInterface()) 
    assert mock.call_count == 1
    app.run()
    assert mock.call_count == 7
