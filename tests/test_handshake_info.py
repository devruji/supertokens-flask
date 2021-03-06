"""
Copyright (c) 2020, VRAI Labs and/or its affiliates. All rights reserved.

This software is licensed under the Apache License, Version 2.0 (the
"License") as published by the Apache Software Foundation.

You may not use this file except in compliance with the License. You may
obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from supertokens_flask.handshake_info import HandshakeInfo
from .utils import (
    reset, setup_st, clean_st, start_st,
    set_key_value_in_config,
    TEST_COOKIE_SECURE_VALUE,
    TEST_COOKIE_SECURE_CONFIG_KEY,
    TEST_SESSION_EXPIRED_STATUS_CODE_VALUE,
    TEST_SESSION_EXPIRED_STATUS_CODE_CONFIG_KEY
)
from supertokens_flask import (
    create_new_session
)
from supertokens_flask.exceptions import SuperTokensGeneralError
from flask import Response


def setup_function(f):
    reset()
    clean_st()
    setup_st()


def teardown_function(f):
    reset()
    clean_st()


def test_core_not_available():
    try:
        create_new_session(Response(''), 'abc', {}, {})
        assert False
    except SuperTokensGeneralError:
        assert True


def test_successful_handshake_and_update_jwt():
    start_st()
    info = HandshakeInfo.get_instance()
    assert info.access_token_path == '/'
    assert info.cookie_domain in {'supertokens.io', 'localhost', None}
    assert isinstance(info.jwt_signing_public_key, str)
    assert isinstance(info.cookie_secure, bool) and not info.cookie_secure
    assert info.refresh_token_path == '/refresh'
    assert isinstance(info.enable_anti_csrf, bool) and info.enable_anti_csrf
    assert isinstance(info.access_token_blacklisting_enabled,
                      bool) and not info.access_token_blacklisting_enabled
    assert isinstance(info.jwt_signing_public_key_expiry_time, int)
    info.update_jwt_signing_public_key_info('test', 100)
    updated_info = HandshakeInfo.get_instance()
    assert updated_info.jwt_signing_public_key == 'test'
    assert updated_info.jwt_signing_public_key_expiry_time == 100


def test_custom_config():
    set_key_value_in_config(
        TEST_SESSION_EXPIRED_STATUS_CODE_CONFIG_KEY,
        TEST_SESSION_EXPIRED_STATUS_CODE_VALUE)
    set_key_value_in_config(
        TEST_COOKIE_SECURE_CONFIG_KEY,
        TEST_COOKIE_SECURE_VALUE)
    start_st()
    assert HandshakeInfo.get_instance(
    ).session_expired_status_code == TEST_SESSION_EXPIRED_STATUS_CODE_VALUE
    assert isinstance(
        HandshakeInfo.get_instance().cookie_secure,
        bool) and HandshakeInfo.get_instance().cookie_secure
