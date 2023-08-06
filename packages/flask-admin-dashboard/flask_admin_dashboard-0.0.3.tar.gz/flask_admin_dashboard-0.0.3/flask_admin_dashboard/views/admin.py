import operator
import os
import pathlib

from flask_admin import AdminIndexView, expose
from flask_login import login_required


# project_root = str(pathlib.Path(__file__).resolve().parents[1])


class AdminView(AdminIndexView):
    def __init__(self, app_root=None):
        super().__init__()
        self.app_root = app_root

    @login_required
    @expose('/')
    def index(self):
        logs = []
        print(f"{self.app_root}/logs/")
        log_files = os.listdir(f"{self.app_root}/logs/")
        index = 0
        for file in log_files:
            index += 1
            this_file = {"name": file.lower(), "index": index}
            with open(f"{self.app_root}/logs/{file}", "r", encoding="utf-8") as f:
                this_file["content"] = f.read()
            logs.append(this_file)
        logs.sort(key=operator.itemgetter('name'))

        for log in logs:
            print(log.get('name'))
        return self.render('admin/logs.html', logs=logs)

    # @login_required
    # @expose('/')
    # def index(self):
    #     info = []
    #     keap = {"name": "Keap", "auth_method": "keap_blueprint.authorize_keap"}
    #     lightspeed = {"name": "Lightspeed", "auth_method": "authorize_lightspeed"}
    #     servicefusion = {"name": "Servicefusion", "auth_method": "authorize_sf"}
    #     keap["authorized"] = self.keap_client.validate_auth()
    #     lightspeed["authorized"] = self.lightspeed_client.validate_auth()
    #     servicefusion["authorized"] = True
    #
    #     info.append(keap)
    #     info.append(lightspeed)
    #     info.append(servicefusion)
    #     return self.render('admin/index.html', info=info)
