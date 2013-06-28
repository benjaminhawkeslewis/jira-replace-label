#!/usr/bin/env python
"""JIRA label updating functions"""

import jira.client
import jira.exceptions

def add_label_by_query(j, jql, label):
    """Add label `label` to issues matching JQL jquery `jql` using JIRA
    client `j`.
    """
    issues = j.search_issues(jql)
    for issue in issues:
        new_labels = issue.fields.labels
        if not label in issue.fields.labels:
            new_labels.append(label)
        yield _label_issue(issue, new_labels)

def remove_label_by_query(j, jql, label_to_remove):
    """Remove label `label` from issues matching JQL jquery `jql` using JIRA
    client `j`.
    """
    issues = j.search_issues(jql)
    for issue in issues:
        new_labels = [label for label in issue.fields.labels
                      if label != label_to_remove]
        yield _label_issue(issue, new_labels)

def replace_label(j, old_label, new_label):
    """Replace label `old_label` with `new_label` on all issues labelled with
    `old_label`.
    """
    issues = j.search_issues('labels in ("%s")' % old_label)
    for issue in issues:
        new_labels = [new_label
                      if label == old_label
                      else label
                      for label in issue.fields.labels]
        yield _label_issue(issue, new_labels)
 
def _label_issue(issue, new_labels):
    """Update JIRA issue `issue` with new labels `new_labels`."""
    original_labels = issue.fields.labels
    try:
        issue.update(labels=new_labels)
        return (issue, original_labels, None)
    except jira.exceptions.JIRAError as exception:
        return (issue, original_labels, exception)
