#!/usr/bin/env python

import jira.client
import jira.exceptions

class JiraLabels(object):

    def add_label_by_query(self, j, jql, label):
        issues = j.search_issues(jql)
        for issue in issues:
            old_labels = issue.fields.labels
            new_labels = issue.fields.labels
            if not label in issue.fields.labels:
                new_labels.append(label)
            yield self._label_issue(issue, new_labels)

    def remove_label_by_query(self, j, jql, label_to_remove):
        issues = j.search_issues(jql)
        for issue in issues:
            old_labels = issue.fields.labels
            new_labels = [label for label in issue.fields.labels if label != label_to_remove]
            yield self._label_issue(issue, new_labels)

    def replace_label(self, j, old_label, new_label):
        issues = j.search_issues('labels in ("%s")' % old_label)
        for issue in issues:
            new_labels = [new_label if label == old_label else label for label in issue.fields.labels]
            yield self._label_issue(issue, new_labels)
 
    def _label_issue(self, issue, new_labels):
        original_labels = issue.fields.labels
        try:
            issue.update(labels=new_labels)
            return (issue, original_labels, None)
        except jira.exceptions.JIRAError as e:
            return (issue, original_labels, e)
