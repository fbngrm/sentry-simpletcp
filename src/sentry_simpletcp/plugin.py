

from django import forms
from django.utils import simplejson
from sentry.utils.safe import safe_execute
from django.utils.translation import ugettext_lazy as _
from sentry.plugins import Plugin

import sentry_simpletcp
import urllib2
from tcp_connection import TCPConnection


class simpleTCPOptionsForm(forms.Form):
    urls = forms.CharField(label=_('Callback URLs'),
        widget=forms.Textarea(attrs={'class': 'span6', 'placeholder': 'https://URL_TO_TCP_SERVER'}),
        help_text=_('Enter callback URLs to TCP server(one per line).'))


class SimpleTCPPlugin(Plugin):
    author = 'Sentry Team'
    author_url = 'https://github.com/getsentry/sentry'
    version = sentry_simpletcp.VERSION
    description = "Integrates web hooks."
    resource_links = [
        ('Bug Tracker', 'https://github.com/getsentry/sentry-webhooks/issues'),
        ('Source', 'https://github.com/getsentry/sentry-webhooks'),
    ]

    slug = 'simpletcp'
    title = _('SimpleTCP')
    conf_title = title
    conf_key = 'simpletcp'
    project_conf_form = simpleTCPOptionsForm

    def is_configured(self, project, **kwargs):
        return bool(self.get_option('urls', project))

    def get_group_data(self, group, event):
        data = {
            'id': str(group.id),
            'checksum': group.checksum,
            'project': group.project.slug,
            'project_name': group.project.name,
            'logger': group.logger,
            'level': group.get_level_display(),
            'culprit': group.culprit,
            'message': event.message,
        }
        data['event'] = event.data or {}
        return data

    def get_tcp_server_urls(self, project):
        return filter(bool, self.get_option('urls', project).strip().splitlines())

    def send_tcp_data(self, url, port, data):
        tcp_connection = TCPConnection()
        tcp_connection.connect(url, port)
        tcp_connection.send(data)
        tcp_connection.close()
        
    def post_process(self, group, event, is_new, is_sample, **kwargs):

        if not self.is_configured(group.project):
            return

        data = simplejson.dumps(self.get_group_data(group, event))
        for url in self.get_tcp_server_urls(group.project):
            try:
                split_url = url.split(':')
                safe_execute(self.send_tcp_data, split_url[0], int(split_url[1]), data)
            except Exception as e:
                print e
