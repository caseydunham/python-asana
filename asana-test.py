"""
Copyright (c) 2012 Casey Dunham <casey.dunham@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import unittest
import functools

import pyasana


API_KEY = "1234abcd"


class ApiTest(unittest.TestCase):

    def setUp(self):
        self._urllib = MockUrllib()
        api = pyasana.Api()
        api.apikey = API_KEY
        api.urllib = self._urllib
        self._api = api

    def testGetWorkspaces(self):
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/workspaces",
            functools.partial(self._openTestData, "workspaces.json"))
        workspaces = self._api.get_workspaces()
        self.assertEqual(1, len(workspaces))

    def testGetUsers(self):
        p = {'opt_fields': 'name,email,worspaces'}
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/users?opt_fields=name,email,workspaces",
            functools.partial(self._openTestData, "users.json"))
        users = self._api.get_users()
        self.assertEqual(2, len(users))
        self.assertEqual(1, len(users[0].workspaces))

    def testGetUser(self):
        userid = 1234
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/users/%s" % userid,
            functools.partial(self._openTestData, "user.json"))
        user = self._api.get_user(userid)
        self.assertEquals(userid, user.id)
        self.assertEquals(2, len(user.workspaces))

    def testGetProjects(self):
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/projects",
            functools.partial(self._openTestData, "projects.json"))
        projects = self._api.get_projects()
        self.assertEqual(2, len(projects))

    def testGetProjectDetail(self):
        project = 14641
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/projects/%s" % project,
            functools.partial(self._openTestData, "project_detail.json"))
        project = self._api.get_project(project)
        self.assertTrue(project.workspace)
        self.assertEqual(652055725497, project.workspace.id)

    def testGerProjectsByWorkspace(self):
        workspace = 15
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/workspaces/%s/projects" % workspace,
            functools.partial(self._openTestData, "projects_for_workspace.json"))
        projects = self._api.get_projects(workspace)
        self.assertEqual(2, len(projects))
        self.assertEqual(99982, projects[0].id)

    def testGetTasksFromProject(self):
        projectid = 9876
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks?project=%s" % projectid,
            functools.partial(self._openTestData, "tasks.json"))
        tasks = self._api.get_tasks(projectid)
        self.assertEqual(2, len(tasks))
        self.assertEqual(1248, tasks[0].id)

    def testGetTasksFromWorkspaceByAssignee(self):
        workspace = 5678
        assignee = 1234
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks?assignee=%s&workspace=%s" % (assignee, workspace),
            functools.partial(self._openTestData, "tasks.json"))
        tasks = self._api.get_tasks(assignee=assignee, workspace=workspace)
        self.assertEqual(2, len(tasks))

    def testGetTasksFromWorkspace(self):
        project = 1337
        workspace = 5678
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks?project=%s&workspace=%s" % (project, workspace),
            functools.partial(self._openTestData, "tasks.json"))
        tasks = self._api.get_tasks(workspace=workspace, project=project)
        self.assertEqual(2, len(tasks))

    def testGetTasksForAssigneeFromWorkspace(self):
        assignee = 1234
        workspace = 5678
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks?assignee=%s&workspace=%s" % (assignee, workspace),
            functools.partial(self._openTestData, "tasks.json"))
        tasks = self._api.get_tasks(assignee=assignee, workspace=workspace)
        self.assertEqual(2, len(tasks))

    def testGetTasksForAssigneeFromProject(self):
        assignee = 1234
        project = 1337
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks?project=%s&assignee=%s" % (project, assignee),
            functools.partial(self._openTestData, "tasks.json"))
        tasks = self._api.get_tasks(project=project, assignee=assignee)
        self.assertEqual(2, len(tasks))

    def testGetTask(self):
        taskid = 24816
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks/%s" % taskid,
            functools.partial(self._openTestData, "task_detail.json"))
        task = self._api.get_task(taskid)
        self.assertEqual(taskid, task.id)
        self.assertEquals("2012-05-07T16:55:37.362Z", task.created_at)
        self.assertEquals(True, task.completed)
        self.assertEquals("2012-05-16T18:44:14.393Z", task.completed_at)

    def testGetStories(self):
        task = 24816
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/tasks/%s/stories" % task,
            functools.partial(self._openTestData, "stories.json"))
        stories = self._api.get_stories(task)
        self.assertEquals(5, len(stories))

    def testGetStoryDetail(self):
        story = 993441745509
        self._urllib.AddHandler("https://app.asana.com/-/api/0.1/stories/%s" % story,
            functools.partial(self._openTestData, "story_detail.json"))
        story = self._api.get_story(story)
        self.assertEquals(993441745509, story.id)
        self.assertTrue(story.target)
        self.assertEquals(24816, story.target.id)

    def _getTestDataPath(self, filename):
        directory = os.path.dirname(os.path.abspath(__file__))
        test_data_dir = os.path.join(directory, "testdata")
        return os.path.join(test_data_dir, filename)

    def _openTestData(self, filename):
        return open(self._getTestDataPath(filename))


class MockUrllib(object):

    def __init__(self):
        self._handlers = {}

    def AddHandler(self, url, callback):
        self._handlers[url] = callback

    def build_opener(self, *handlers):
        return MockOpener(self._handlers)


class MockOpener(object):

    def __init__(self, handlers):
        self._handlers = handlers

    def open(self, url, data=None):
        if url in self._handlers:
            return self._handlers[url]()
        else:
            raise Exception("Unexpected URL %s" % url)


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(ApiTest))
    return suite


if __name__ == '__main__':
    unittest.main()
