import operator
import os
import pathlib
from flask_admin import BaseView, expose
from flask_login import login_required

project_root = str(pathlib.Path(__file__).resolve().parents[1])


class LogView(BaseView):
    @login_required
    @expose('/')
    def index(self):
        logs = []
        log_files = os.listdir(f"{project_root}/logs/")
        index = 0
        for file in log_files:
            index += 1
            this_file = {"name": file.lower(), "index": index}
            with open(f"{project_root}/logs/{file}", "r", encoding="utf-8") as f:
                this_file["content"] = f.read()
            logs.append(this_file)
        logs.sort(key=operator.itemgetter('name'))

        for log in logs:
            print(log.get('name'))
        return self.render('admin/logs.html', logs=logs)

