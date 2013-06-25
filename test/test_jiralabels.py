import unittest
import jiralabels
import jira
from mock import Mock

class TestJiraLabels(unittest.TestCase):

    def setUp(self):
        self.jiralabels = jiralabels.JiraLabels()
    
    def test_add_label_by_query_with_no_results(self):
        j = Mock()
        jql = 'assignee = john.doe'
        label = 'somelabel'
        j.search_issues = Mock(return_value = [])
        self.jiralabels.add_label_by_query(j, jql, label)
        j.search_issues.assert_called_once_with(jql)

    def test_add_label_by_query_with_results(self):
        j = Mock()
        jql = 'assignee = john.doe'
        label = 'somelabel'
        issue = Mock()
        issue.fields = Mock()
        issue.fields.labels = ['alpha', 'beta', 'gamma']
        issue.update = Mock() 
        j.search_issues = Mock(return_value = [issue])
        self.jiralabels.add_label_by_query(j, jql, label)
        j.search_issues.assert_called_once_with(jql)
        issue.update.assert_called_once_with(labels=['alpha', 'beta', 'gamma', 'somelabel'])

    def test_remove_label_by_query_with_results(self):
        j = Mock()
        jql = 'assignee = john.doe'
        label_to_remove = 'removeme'
        issue = Mock()
        issue.fields = Mock()
        issue.fields.labels = ['alpha', label_to_remove, 'gamma']
        issue.update = Mock() 
        j.search_issues = Mock(return_value = [issue])
        self.jiralabels.remove_label_by_query(j, jql, label_to_remove)
        j.search_issues.assert_called_once_with(jql)
        issue.update.assert_called_once_with(labels=['alpha', 'gamma'])

    def test_replace_label_with_results(self):
        j = Mock()
        old_label = 'old'
        new_label = 'new'
        issue = Mock()
        issue.fields = Mock()
        issue.fields.labels = ['alpha', old_label, 'gamma']
        issue.update = Mock() 
        j.search_issues = Mock(return_value = [issue])
        self.jiralabels.replace_label(j, old_label, new_label)
        j.search_issues.assert_called_once_with('labels in ("old")')
        issue.update.assert_called_once_with(labels=['alpha', new_label, 'gamma'])


