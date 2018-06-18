# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


import flask_admin
from flask import Blueprint, request, json
from flask import render_template
from flask_security import logout_user
from werkzeug.utils import redirect

from dashboard.application.conf.config import *
from dashboard.application.dashboard.views.api_token_view import ApiTokenView
from dashboard.application.dashboard.views.home_view import HomeView
from dashboard.application.dashboard.views.logs_view import LogsView
from dashboard.application.dashboard.views.messages_view import MessageView
from dashboard.application.dashboard.views.ml_model_publisher_view import \
    MLModelPublisherView
from dashboard.application.dashboard.views.ml_model_view import MlModelView
from dashboard.application.dashboard.views.user_admin_view import UserAdmin, \
    RoleAdmin
from dashboard.domain.entities.auth.api_token_model import Token
from dashboard.domain.entities.auth.login_model import User, Role
from dashboard.domain.entities.logs import Logs
from dashboard.domain.entities.ml_model import MlModel
from dashboard.domain.interactor.logs.get_time_line_events import \
    GetTimeLineEvents
from dashboard.domain.interactor.logs.get_workers_load_model_status import \
    GetWorkersLoadModelStatus
from dashboard.domain.interactor.logs.save_model_log_event import \
    SaveModelLogEvent
from dashboard.domain.interactor.messages.user_messaging import UserMessaging
from dashboard.domain.interactor.orchestation.orchestation_interator import \
    OrchestationInteractor
from dashboard.domain.interactor.users.current_user import CurrentUser
from dashboard.domain.interactor.users.users_privileges import UsersPrivileges
from dashboard.domain.repositories.logs_repository import LogsRepository
from dashboard.domain.repositories.messages_repository import MessageRepository
from dashboard.domain.repositories.model_repository import ModelRepository
from dashboard.domain.repositories.worker_repository import WorkerRepository


class Dashboard:
    def __init__(
            self, app, worker_repository: WorkerRepository,
            model_repository: ModelRepository,
            save_model_log_event: SaveModelLogEvent,
            message_repository: MessageRepository,
            logs_repository: LogsRepository,
            orchestation_interactor: OrchestationInteractor,
            users_privileges: UsersPrivileges, current_user: CurrentUser,
            user_messaging: UserMessaging,
            get_time_line_events: GetTimeLineEvents,
            get_workers_load_model_status: GetWorkersLoadModelStatus):
        self.get_workers_load_model_status = get_workers_load_model_status
        self.worker_repository = worker_repository
        self.model_repository = model_repository
        self.save_model_log_event = save_model_log_event
        self.get_time_line_events = get_time_line_events
        self.message_repository = message_repository
        self.current_user = current_user
        self.users_privileges = users_privileges
        self.orchestation_interactor = orchestation_interactor
        self.logs_repository = logs_repository
        self.user_messaging = user_messaging
        self.app = app

        self.dashboard_blueprint = Blueprint('dashboard', __name__,
                                             template_folder='templates',
                                             url_prefix='/dashboard')

        app.jinja_env.globals.update(
            pending_messages=self.user_messaging.get_pending_messages)

        @self.dashboard_blueprint.route('/logout')
        def logout_view():
            logout_user()
            return redirect(request.url_root + "dashboard/")

        @self.dashboard_blueprint.route('/info', methods=('GET',))
        def get_info():
            data = {"zookeper": ZOOKEEPER,
                    "mongo": MONGO_CONNECTION_URI,
                    "mongo_database": MONGO_DATABASE,
                    "zookeper_directory": PROJECT,
                    "dashboard_port": SERVICE_PORT,
                    "dashboard_title": dashboard_home_title,
                    }
            return json.dumps(data), 200, {'ContentType': 'application/json'}

        @self.app.errorhandler(404)
        def page_not_found(e):
            return render_template('404.html'), 404

        self._initialize_views()

    def get_blueprint(self):
        return self.dashboard_blueprint

    def _initialize_views(self):
        self.app.jinja_env.globals.update(
            pending_messages=self.user_messaging.get_pending_messages)

        admin = flask_admin.Admin(
            self.app,
            name=dashboard_home_title,
            base_template='adminlte_base.html',
            template_mode="bootstrap3",
            index_view=HomeView(
                get_line_time_events=self.get_time_line_events,
                get_workers_load_model_status=self.get_workers_load_model_status,
                name="Dashboard",
                url=self.dashboard_blueprint.url_prefix,
                menu_icon_type='fa',
                template='home/index.html',
                menu_icon_value='fa-dashboard'),
            category_icon_classes={
                'Access': 'glyphicon glyphicon-user',
                'PreProcess': 'glyphicon glyphicon-equalizer',
            })

        # Add view
        admin.add_view(
            MlModelView(MlModel, model_repository=self.model_repository,
                        current_user=self.current_user,
                        save_model_log_event=self.save_model_log_event,
                        name='Models',
                        menu_icon_type='fa', menu_icon_value='fa-flask'))
        admin.add_view(UserAdmin(User, name='User', menu_icon_type='fa',
                                 menu_icon_value='fa-users'))
        admin.add_view(RoleAdmin(Role, name='Roles', menu_icon_type='fa',
                                 menu_icon_value='fa-address-book'))
        admin.add_view(
            ApiTokenView(Token, name='Api Token', menu_icon_type='fa',
                         menu_icon_value='fa-key'))
        admin.add_view(MLModelPublisherView(
            name='Model publisher',
            users_privilages=self.users_privileges,
            orchestation_interactor=self.orchestation_interactor,
            get_workers_load_model_status=self.get_workers_load_model_status,
            current_user=self.current_user,
            menu_icon_type='fa',
            menu_icon_value='fa-desktop'))
        admin.add_view(
            MessageView(
                name="Messages", menu_icon_type='fa',
                menu_icon_value='fa-inbox',
                endpoint="messages",
                message_repository=self.message_repository,
                user_messaging=self.user_messaging,
                current_user=self.current_user))

        admin.add_view(
            LogsView(
                Logs, current_user=self.current_user, name="Logs",
                menu_icon_type='fa',
                menu_icon_value='fa-archive'))
