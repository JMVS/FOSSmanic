#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    unmanic.session.py

    Copyright:
           Copyright (C) Josh Sunnex - All Rights Reserved

           Permission is hereby granted, free of charge, to any person obtaining a copy
           of this software and associated documentation files (the "Software"), to deal
           in the Software without restriction, including without limitation the rights
           to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
           copies of the Software, and to permit persons to whom the Software is
           furnished to do so, subject to the following conditions:

           The above copyright notice and this permission notice shall be included in all
           copies or substantial portions of the Software.

           THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
           EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
           MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
           IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
           DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
           OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
           OR OTHER DEALINGS IN THE SOFTWARE.

"""
import uuid
import time

from unmanic import config
from unmanic.libs.logs import UnmanicLogging
from unmanic.libs.singleton import SingletonType
from unmanic.libs.unmodels import Installation


class RemoteApiException(Exception):
    """
    RemoteApiException
    Custom exception for errors contacting the remote Unmanic API
    """
    def __init__(self, message, status_code):
        pass


class Session(object, metaclass=SingletonType):
    """
    Session

    Manages the Unmanic applications session for UUID persistence.
    """
    level = 5
    library_count = 999
    link_count = 999
    picture_uri = ''
    name = ''
    email = ''
    created = None
    last_check = None
    uuid = None
    user_access_token = None
    application_token = None

    def __init__(self, *args, **kwargs):
        self.logger = UnmanicLogging.get_logger(name=__class__.__name__)
        self.timeout = 30
        self.dev_api = kwargs.get('dev_api', None)
        self.requests_session = None
        self.token_poll_task = None
        self.logger.info('Initialising new session object')
        self.created = time.time()
        self.last_check = None

    def __created_older_than_x_days(self, days=1):
        return False

    def __check_session_valid(self):
        return True

    def __update_created_timestamp(self):
        pass

    def __fetch_installation_data(self):
        db_installation = Installation()
        try:
            current_installation = db_installation.select().order_by(Installation.id.asc()).limit(1).get()
            self.uuid = str(current_installation.uuid)
        except Exception:
            self.uuid = str(uuid.uuid4())
            self.__store_installation_data()

    def __store_installation_data(self, force_save_access_token=False):
        if self.uuid:
            db_installation = Installation.get_or_none(uuid=self.uuid)
            if not db_installation:
                db_installation = Installation.create(uuid=self.uuid)
            else:
                db_installation.uuid = self.uuid
                db_installation.save()

    def __configure_log_forwarding(self, session_valid=False):
        pass

    def __reset_session_installation_data(self):
        pass

    def __update_session_auth(self, access_token=None):
        pass

    def __clear_session_auth(self):
        pass

    def get_installation_uuid(self):
        if not self.uuid:
            self.__fetch_installation_data()
        return self.uuid

    def get_supporter_level(self):
        return self.level

    def get_site_url(self):
        return "http://localhost"

    def set_full_api_url(self, api_prefix, api_version, api_path):
        return "http://localhost/api/v1/mock"

    def api_get(self, api_prefix, api_version, api_path):
        pass

    def api_post(self, api_prefix, api_version, api_path, data):
        pass

    def get_access_token(self):
        return False

    def verify_token(self):
        return False

    def fetch_user_data(self):
        pass

    def auth_user_account(self, force_checkin=False):
        return True

    def auth_trial_account(self):
        return True

    def register_unmanic(self, force=False):
        self.__fetch_installation_data()
        self.__store_installation_data()
        return True

    def sign_out(self, remote=True):
        return True

    def get_sign_out_url(self):
        return "http://localhost/api/v1/mock/logout"

    def init_device_auth_flow(self):
        return False

    def poll_for_app_token(self, device_code, interval, expires_in):
        return False

    def get_patreon_login_url(self):
        return "http://localhost/api/v1/mock/login"

    def get_github_login_url(self):
        return "http://localhost/api/v1/mock/login"
        
    def get_discord_login_url(self):
        return "http://localhost/api/v1/mock/login"
        
    def get_patreon_sponsor_page(self):
        return False
