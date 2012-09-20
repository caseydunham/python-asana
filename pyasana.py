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

__author__ = 'casey.dunham@gmail.com'
__version__ = '0.0.1-devel'


import urllib2
import urlparse
import json
import base64

from urllib import urlencode


class AsanaError(Exception):

    @property
    def message(self):
        return self.args[0]


class User(object):

    def __init__(self, id=None, name=None, email=None, workspaces=None):
        self.id = id
        self.name = name
        self.email = email
        self.workspaces = workspaces

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def workspaces(self):
        return self._workspaces

    @workspaces.setter
    def workspaces(self, value):
        self._workspaces = value

    @staticmethod
    def new_from_json(data):
        user = User()
        if "id" in data:
            user.id = data["id"]
        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "workspaces" in data:
            user.workspaces = [Workspace.new_from_json(x) for x in data["workspaces"]]
        return user


class Project(object):

    def __init__(self, id=None, name=None, created_at=None, modified_at=None, notes=None,
                 archived=None, workspace=None, followers=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.modified_at = modified_at
        self.notes = notes
        self.archived = archived
        self.workspace = workspace
        self.followers = followers

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

    @property
    def archived(self):
        return self._archived

    @archived.setter
    def archived(self, value):
        self._archived = value

    @property
    def workspace(self):
        return self._workspace

    @workspace.setter
    def workspace(self, value):
        self._workspace = value

    @property
    def followers(self):
        return self._followers

    @followers.setter
    def followers(self, value):
        self._followers = value

    @staticmethod
    def new_from_json(data):
        project = Project()
        if "id" in data:
            project.id = data["id"]
        if "name" in data:
            project.name = data["name"]
        if "created_at" in data:
            project.created_at = data["created_at"]
        if "modified_at" in data:
            project.modified_at = data["modified_at"]
        if "archived" in data:
            project.archived = data["archived"]
        if "workspace" in data:
            project.workspace = Workspace.new_from_json(data["workspace"])
        if "followers" in data:
            project.followers = [User.new_from_json(x) for x in data["followers"]]
        return project


class Workspace(object):

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @staticmethod
    def new_from_json(data):
        workspace = Workspace()
        if "id" in data:
            workspace.id = data["id"]
        if "name" in data:
            workspace.name = data["name"]
        return workspace


class Task(object):

    def __init__(self, id=None, assignee=None, created_at=None, completed=None, completed_at=None,
                 followers=None, modified_at=None, name=None, notes=None, projects=None,
                 assignee_status=None, workspace=None):
        self.id = id
        self.assignee = assignee
        self.created_at = created_at
        self.completed = completed
        self.completed_at = completed_at
        self.followers = followers
        self.modified_at = modified_at
        self.name = name
        self.notes = notes
        self.projects = projects
        self.assignee_status = assignee_status
        self.workspace = workspace

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def assignee(self):
        return self._assignee

    @assignee.setter
    def assignee(self, value):
        self._assignee = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        self._completed = value

    @property
    def completed_at(self):
        return self._completed_at

    @completed_at.setter
    def completed_at(self, value):
        self._completed_at = value

    @property
    def followers(self):
        return self._followers

    @followers.setter
    def followers(self, value):
        self._followers = value

    @property
    def modified_at(self):
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value):
        self._modified_at = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def notes(self):
        return self._notes

    @notes.setter
    def notes(self, value):
        self._notes = value

    @property
    def projects(self):
        return self._projects

    @projects.setter
    def projects(self, value):
        self._projects = value

    @property
    def assignee_status(self):
        return self._assignee_status

    @assignee_status.setter
    def assignee_status(self, value):
        self._assignee_status = value

    @property
    def workspace(self):
        return self._workspace

    @workspace.setter
    def workspace(self, value):
        self._workspace = value

    @staticmethod
    def new_from_json(data):
        task = Task()
        if "id" in data:
            task.id = data["id"]
        if "name" in data:
            task.name = data["name"]
        if "created_at" in data:
            task.created_at = data["created_at"]
        if "completed" in data:
            task.completed = data["completed"]
        if "completed_at" in data:
            task.completed_at = data["completed_at"]
        if "modified_at" in data:
            task.modified_at = data["modified_at"]
        if "notes" in data:
            task.notes = data["notes"]
        if "followers" in data:
            task.followers = [User.new_from_json(x) for x in data["followers"]]
        if "assignee_status" in data:
            task.assignee_status = data["assignee_status"]
        if "workspace" in data:
            task.workspace = Workspace.new_from_json(data["workspace"])
        if "projects" in data:
            task.projects = [Project.new_from_json(x) for x in data["projects"]]
        return task


class Story(object):

    def __init__(self, id=None, created_at=None, type=None, text=None, created_by=None,
                 target=None, source=None):
        self.id = id
        self.created_at = created_at
        self.type = type
        self.text = text
        self.created_by = created_by
        self.target = target
        self.source = source

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def created_by(self):
        return self._created_by

    @created_by.setter
    def created_by(self, value):
        self._created_by = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @staticmethod
    def new_from_json(data):
        story = Story()
        if "id" in data:
            story.id = data["id"]
        if "created_at" in data:
            story.created_at = data["created_at"]
        if "type" in data:
            story.type = data["type"]
        if "text" in data:
            story.text = data["text"]
        if "created_by" in data:
            story.created_by = User.new_from_json(data["created_by"])
        if "target" in data:
            story.target = Task.new_from_json(data["target"])
        if "source" in data:
            story.source = data["source"]
        return story


class Api(object):

    def __init__(self, apikey=None):
        self.apikey = apikey
        self.urllib = urllib2
        self._init_request_headers()

    @property
    def apikey(self):
        return self._apikey

    @apikey.setter
    def apikey(self, value):
        self._apikey = value

    @property
    def urllib(self):
        return self._urllib

    @urllib.setter
    def urllib(self, value):
        self._urllib = value

    def get_workspaces(self):
        url = "https://app.asana.com/-/api/0.1/workspaces"
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return [Workspace.new_from_json(x) for x in data["data"]]

    def get_projects(self, workspace=None):
        if workspace:
            url = "https://app.asana.com/-/api/0.1/workspaces/%s/projects" % workspace
        else:
            url = "https://app.asana.com/-/api/0.1/projects"
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return [Project.new_from_json(x) for x in data["data"]]

    def get_project(self, project):
        url = "https://app.asana.com/-/api/0.1/projects/%s" % project
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return Project.new_from_json(data["data"])

    def get_users(self):
        url = "https://app.asana.com/-/api/0.1/users?opt_fields=name,email,workspaces"
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return [User.new_from_json(x) for x in data["data"]]

    def get_user(self, userid=None):
        url = "https://app.asana.com/-/api/0.1/users/%s" % userid
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return User.new_from_json(data["data"])

    def get_tasks(self, project=None, workspace=None, assignee=None):
        params = {}
        if project:
            params["project"] = project
        if workspace:
            params["workspace"] = workspace
        if assignee:
            params["assignee"] = assignee

        # can retrieve all tasks for a project without any other data
        # if assignee is specified, need a project or workspace
        # if workspace is specified need an assignee
        if workspace:
            if project is None and assignee is None:
                raise AsanaError("Need to specify a project or assignee")

        if assignee:
            if workspace is None and project is None:
                raise AsanaError("Need to specify a workspace or project")

        url = "https://app.asana.com/-/api/0.1/tasks"
        json_data = self._fetch_url(url, parameters=params)
        data = json.loads(json_data)
        return [Task.new_from_json(x) for x in data["data"]]

    def get_task(self, taskid):
        url = "https://app.asana.com/-/api/0.1/tasks/%s" % taskid
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return Task.new_from_json(data["data"])

    def get_stories(self, taskid):
        url = "https://app.asana.com/-/api/0.1/tasks/%s/stories" % taskid
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return [Story.new_from_json(x) for x in data["data"]]

    def get_story(self, storyid):
        url = "https://app.asana.com/-/api/0.1/stories/%s" % storyid
        json_data = self._fetch_url(url)
        data = json.loads(json_data)
        return Story.new_from_json(data["data"])

    def _fetch_url(self, url, post_data=None, parameters=None):
        url = self._build_url(url, parameters)
        opener = self._get_opener(url, self.apikey)
        data = opener.open(url).read()
        return data

    def _build_url(self, url, parameters=None):
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
        if parameters and len(parameters) > 0:
            query = self._encode_parameters(parameters)

        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

    def _encode_parameters(self, parameters=None):
        if parameters:
            return urlencode(dict([(k, self._utf8_encode(v)) for k, v in parameters.items() if v is not None]))
        return None

    def _utf8_encode(self, s):
        return unicode(s).encode('utf-8')

    def _init_request_headers(self, request_headers=None):
        self._request_headers = {}
        if request_headers:
            self._request_headers = request_headers

    def _add_authorization_header(self, apikey=None):
        if apikey:
            authorization = "%s:" % apikey
            self._request_headers["Authorization"] = "Basic %s" % base64.b64encode(authorization)

    def _get_opener(self, url, apikey=None):
        if not apikey:
            raise AsanaError("No API Key set!")
        self._add_authorization_header(apikey)
        opener = self.urllib.build_opener()
        opener.addheaders = self._request_headers.items()
        return opener


