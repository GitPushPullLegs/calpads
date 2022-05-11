import json
from collections import deque
from urllib.parse import urlsplit, urljoin

import requests
from lxml import etree

from src.extensions.core import Core
from src.extensions.student import Student


class CALPADS:
    BASE_URL = "https://www.calpads.org/"

    def __init__(self, username: str, password: str):
        self.credentials = dict(
            Username=username,
            Password=password
        )
        self.is_connected = False
        self.visit_history = deque(maxlen=10)

        self.core = Core(self)
        self.student = Student(self)

    @property
    def _session(self):
        if not hasattr(self, "_client"):
            self._client = requests.session()
            self._client.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/70.0.3538.77 "
                              "Safari/537.36"
            })
            self._client.hooks["response"].append(self._event_hooks)
            try:
                self.is_connected = self._login()
            except RecursionError as err:
                print(f"Failed to login. Error: {err}")

        return self._client

    def get_resource(self, endpoint: str):
        response = self._session.get(urljoin(self.BASE_URL, endpoint))
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            response.raise_for_status()

    def _login(self):
        self._session.get(self.BASE_URL)
        return self.visit_history[-1].status_code == 200 and self.visit_history[-1].url == self.BASE_URL

    def _event_hooks(self, r, *args, **kwargs):
        """
        Authenticates a rest by appending the form data based on the authentication path.
        :param r: The session request.
        """
        scheme, netloc, path, query, frag = urlsplit(r.url)
        if path == '/Account/Login' and r.status_code == 200:
            self._session.cookies.update(r.cookies.get_dict())
            init_root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
            self.credentials['__RequestVerificationToken'] = \
                init_root.xpath("//input[@name='__RequestVerificationToken']")[0].get('value')
            self.credentials['ReturnUrl'] = init_root.xpath("//input[@id='ReturnUrl']")[0].get('value')
            self.credentials['AgreementConfirmed'] = 'True'
            self._session.post(r.url, data=self.credentials)
        elif path in ['/connect/authorize/callback', '/connect/authorize'] and r.status_code == 200:
            self._session.cookies.update(r.cookies.get_dict())
            login_root = etree.fromstring(r.text, parser=etree.HTMLParser(encoding='utf8'))
            openid_form_data = {input_.attrib.get('name'): input_.attrib.get('value') for input_ in
                                login_root.xpath('//input')}
            action_url = login_root.xpath('//form')[0].attrib.get('action')
            scheme, netloc, path, query, frag = urlsplit(action_url)
            if not scheme and not netloc:
                self._session.post(urljoin(self.BASE_URL, action_url), data=openid_form_data)
            else:
                self._session.post(action_url, data=openid_form_data)
        else:
            self.visit_history.append(r)
            return r
