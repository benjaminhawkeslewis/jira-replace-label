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
        j.search_issues = Mock(return_value = [issue] )
        self.jiralabels.add_label_by_query(j, jql, label)
        j.search_issues.assert_called_once_with(jql)
        issue.update.assert_called_once_with(labels=['alpha', 'beta', 'gamma', 'somelabel'])
