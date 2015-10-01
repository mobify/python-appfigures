# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import


class AppFigureObject(object):

    def __init__(self, json):
        super(AppFigureObject, self).__init__()
        self._json_data = json

        if self._json_data:
            self._load_from_json(self._json_data)

    def _load_from_json(self, json):
        raise NotImplementedError()

    @classmethod
    def from_json(cls, json):
        return cls(json)
