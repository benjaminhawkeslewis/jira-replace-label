from distutils.core import setup

setup(
    name='jira-replace-label',
    version='0.1',
    author='Benjamin Hawkes-Lewis',
    author_email='contact@benjaminhawkeslewis.com',
    maintainer='Benjamin Hawkes-Lewis',
    maintainer_email='contact@benjaminhawkeslewis.com',
    description="Script to replace labels in JIRA without side effects of destroying other labels.",
    scripts=['bin/jira-replace-label'],
    requires=['jira (>0.13)']
)    
