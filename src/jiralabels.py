#!/usr/bin/env python

import jira.client
import jira.exceptions
import requests.exceptions
import sys
import signal
import argparse
import getpass

class Event(object):
    
    def __init__(self, issue):
        self.issue = issue

class ErrorEvent(Event):
    
    def __init__(self, issue, exception):
        self.exception = exception
        super(ErrorEvent, self).__init__(issue)

class LabelEvent(Event):
    
    def __init__(self, issue, old_labels):
        self.old_labels = old_labels
        super(LabelEvent, self).__init__(issue)

class JiraLabels(object):

    def __init__(self):
        self._listeners = {}

    def add_listener(self, event_class, callback):
        if not event_class in self._listeners:
            self._listeners[event_class] = []
        self._listeners[event_class].append(callback)

    def add_label_by_query(self, j, jql, label):
        issues = j.search_issues(jql)
        for issue in issues:
            old_labels = issue.fields.labels
            new_labels = issue.fields.labels
            if not label in issue.fields.labels:
                new_labels.append(label)
            self._label_issue(issue, new_labels)

    def remove_label_by_query(self, j, jql, label_to_remove):
        issues = j.search_issues(jql)
        for issue in issues:
            old_labels = issue.fields.labels
            new_labels = [label for label in issue.fields.labels if label != label_to_remove]
            self._label_issue(issue, new_labels)

    def replace_label(self, j, old_label, new_label):
        issues = j.search_issues('labels in ("%s")' % old_label)
        for issue in issues:
            new_labels = [new_label if label == old_label else label for label in issue.fields.labels]
            self._label_issue(issue, new_labels)

    def _label_issue(self, issue, new_labels):
        old_labels = issue.fields.labels
        try:
            issue.update(labels=new_labels)
            self._update_listeners(LabelEvent(issue, old_labels))
        except jira.exceptions.JIRAError as e:
            self._update_listeners(ErrorEvent(issue, e))
         
    def _update_listeners(self, event):
        if event.__class__.__name__ in self._listeners:
            for callback in self._listeners[event.__class__.__name__]:
                callback(event) 
