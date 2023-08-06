#!/usr/bin/env python
# encoding: utf-8
import abc

from gitflow_api.config.config import Config

class Deploy(object):
    __metaclass__ = abc.ABCMeta

    config = Config()

    def __init__(self, classtype):
        self._type = classtype

    @abc.abstractmethod
    def deploy(self):
        pass