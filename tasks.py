import sys

from celery import Celery, states
from celery.exceptions import Ignore
from behave.__main__ import main as behave_main

from io import StringIO

app = Celery("tasks", broker="pyamqp://rabbitmq:rabbitmq@rabbit//")
app.conf.task_default_queue = "behave"
app.conf.send_events = True
app.conf.send_task_sent_event = True

REPLACE_CHARS = ("Scenario: ", "Scenario Outline: ", "\r")


@app.task(bind=True)
def delegate_test(self, scenario):

    def replace_char(string):
        for char in REPLACE_CHARS:
            string = string.replace(char, '')
        return string

    argstable = [
        'behave/features/django_admin/',
        '-n', '{}{}'.format(replace_char(scenario), '$' if 'Outline' not in scenario else ''),
        '-f', 'allure_behave.formatter:AllureFormatter',
        '-f', 'pretty',
        '-o', '%allure_result_folder%',
        '--no-skipped']

    old_stdout = sys.stdout
    io = StringIO()

    sys.stdout = io
    behave_main(argstable)
    sys.stdout = old_stdout
    behave_result = io.getvalue()

    if "1 scenario passed" not in behave_result:
        # manually update the task state
        self.update_state(state=states.FAILURE, meta=behave_result)

        raise Exception(behave_result)
    return "Pass"

