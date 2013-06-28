"""
Copyright (c) 2012 Casey Dunham <casey.dunham@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
        partial = functools.partial(self._openTestData, "workspaces.json")
        url = "%s/workspaces" % self._api.API_BASE
        self._urllib.AddHandler(url, partial)
        workspaces = self._api.get_workspaces()
        self.assertEqual(1, len(workspaces))

    def testGetUsers(self):
        partial = functools.partial(self._openTestData, "users.json")
        url = "%s/users?opt_fields=name,email,workspaces" % self._api.API_BASE
        self._urllib.AddHandler(url, partial)
        users = self._api.get_users()
        self.assertEqual(2, len(users))
        self.assertEqual(1, len(users[0].workspaces))

    def testGetUser(self):
        userid = 1234
        partial = functools.partial(self._openTestData, "user.json")
        url = "%s/users/%s" % (self._api.API_BASE, userid)
        self._urllib.AddHandler(url, partial)
        user = self._api.get_user(userid)
        self.assertEquals(userid, user.id)
        self.assertEquals(2, len(user.workspaces))

    def testGetProjects(self):
        partial = functools.partial(self._openTestData, "projects.json")
        url = "%s/projects" % self._api.API_BASE
        self._urllib.AddHandler(url, partial)
        projects = self._api.get_projects()
        self.assertEqual(2, len(projects))

    def testGetProjectDetail(self):
        project = 14641
        partial = functools.partial(self._openTestData, "project_detail.json")
        url = "%s/projects/%s" % (self._api.API_BASE, project)
        self._urllib.AddHandler(url, partial)
        project = self._api.get_project(project)
        self.assertTrue(project.workspace)
        self.assertEqual(652055725497, project.workspace.id)

    def testGerProjectsByWorkspace(self):
        workspace = 15
        partial = functools.partial(self._openTestData, "projects_for_workspace.json")
        url = "%s/workspaces/%s/projects" % (self._api.API_BASE, workspace)
        self._urllib.AddHandler(url, partial)
        projects = self._api.get_projects(workspace)
        self.assertEqual(2, len(projects))
        self.assertEqual(99982, projects[0].id)

    def testCreateProject(self):
        partial = functools.partial(self._openTestData, "create_project.json")
        url = "%s/projects" % self._api.API_BASE
        self._urllib.AddHandler(url, partial)
        workspace = pyasana.Workspace()
        workspace.id = 498346170860
        project = self._api.create_project(workspace, "api test project")
        self.assertEqual(4018163373477, project.id)
        self.assertEqual("api test project", project.name)

    def testGetTasksFromProject(self):
        projectid = 9876
        partial = functools.partial(self._openTestData, "tasks.json")
        url = "%s/tasks?project=%s" % (self._api.API_BASE, projectid)
        self._urllib.AddHandler(url, partial)
        tasks = self._api.get_tasks(projectid)
        self.assertEqual(2, len(tasks))
        self.assertEqual(1248, tasks[0].id)

    def testGetTasksFromWorkspaceByAssignee(self):
        workspace = 5678
        assignee = 1234
        partial = functools.partial(self._openTestData, "tasks.json")
        url = "%s/tasks?assignee=%s&workspace=%s" % (self._api.API_BASE, assignee, workspace)
        self._urllib.AddHandler(url, partial)
        tasks = self._api.get_tasks(assignee=assignee, workspace=workspace)
        self.assertEqual(2, len(tasks))

    def testGetTasksFromWorkspace(self):
        project = 1337
        workspace = 5678
        partial = functools.partial(self._openTestData, "tasks.json")
        url = "%s/tasks?project=%s&workspace=%s" % (self._api.API_BASE, project, workspace)
        self._urllib.AddHandler(url, partial)
        tasks = self._api.get_tasks(workspace=workspace, project=project)
        self.assertEqual(2, len(tasks))

    def testGetTasksForAssigneeFromWorkspace(self):
        assignee = 1234
        workspace = 5678
        partial = functools.partial(self._openTestData, "tasks.json")
        url = "%s/tasks?assignee=%s&workspace=%s" % (self._api.API_BASE, assignee, workspace)
        self._urllib.AddHandler(url, partial)
        tasks = self._api.get_tasks(assignee=assignee, workspace=workspace)
        self.assertEqual(2, len(tasks))

    def testGetTasksForAssigneeFromProject(self):
        assignee = 1234
        project = 1337
        partial = functools.partial(self._openTestData, "tasks.json")
        url = "%s/tasks?project=%s&assignee=%s" % (self._api.API_BASE, project, assignee)
        self._urllib.AddHandler(url, partial)
        tasks = self._api.get_tasks(project=project, assignee=assignee)
        self.assertEqual(2, len(tasks))

    def testGetTask(self):
        taskid = 24816
        partial = functools.partial(self._openTestData, "task_detail.json")
        url = "%s/tasks/%s" % (self._api.API_BASE, taskid)
        self._urllib.AddHandler(url, partial)
        task = self._api.get_task(taskid)
        self.assertEqual(taskid, task.id)
        self.assertEquals("2012-05-07T16:55:37.362Z", task.created_at)
        self.assertEquals(True, task.completed)
        self.assertEquals("2012-05-16T18:44:14.393Z", task.completed_at)

    def testGetTaskTags(self):
        taskid = 24816
        partial = functools.partial(self._openTestData, "task_tags.json")
        url = "%s/tasks/%s/tags" % (self._api.API_BASE, taskid)
        self._urllib.AddHandler(url, partial)
        tags = self._api.get_task_tags(taskid)
        self.assertEqual(2, len(tags))
        self.assertEqual("Rich Gold", tags[0].name)
        self.assertEqual("Honey Shrimp", tags[1].name)

    def testGetTag(self):
        tagid = 5007
        partial = functools.partial(self._openTestData, "tag_detail.json")
        url = "%s/tags/%s" % (self._api.API_BASE, tagid)
        self._urllib.AddHandler(url, partial)
        tag = self._api.get_tag(tagid)
        self.assertEqual(tagid, tag.id)
        self.assertEqual("2013-06-28T11:55:33.333Z", tag.created_at)
        self.assertEqual("Rich Gold", tag.name)
        self.assertEqual(2, len(tag.followers))

    def testGetStories(self):
        task = 24816
        partial = functools.partial(self._openTestData, "stories.json")
        url = "%s/tasks/%s/stories" % (self._api.API_BASE, task)
        self._urllib.AddHandler(url, partial)
        stories = self._api.get_stories(task)
        self.assertEquals(5, len(stories))

    def testGetStoryDetail(self):
        story = 993441745509
        partial = functools.partial(self._openTestData, "story_detail.json")
        url = "%s/stories/%s" % (self._api.API_BASE, story)
        self._urllib.AddHandler(url, partial)
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
