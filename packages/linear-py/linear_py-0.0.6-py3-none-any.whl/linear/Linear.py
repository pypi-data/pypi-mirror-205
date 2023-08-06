import json
import requests

from .Exceptions import LinearQueryException

class Linear:
    def __init__(self, LINEAR_API_KEY=''):
        self.set_url('https://api.linear.app/graphql')
        self.set_api_key(LINEAR_API_KEY)
        self.headers = {
            "Authorization" : self.LINEAR_API_KEY
        }
        pass

    def set_url(self, url):
        self.graphql_url = url

    def set_api_key(self, LINEAR_API_KEY):
        self.LINEAR_API_KEY = LINEAR_API_KEY

    def query_grapql(self, query):
        r = requests.post(self.graphql_url, json={
            "query": query
        }, headers=self.headers)

        response = json.loads(r.content)

        if 'errors' in response:
            raise LinearQueryException(response["errors"])

        return response

    def query_basic_resource(self, resource=''):
        resource_response = self.query_grapql(
            """
                query Resource {"""+resource+"""{nodes{id,name}}}
            """
        )

        return resource_response["data"][resource]["nodes"]

    def create_issue(self, title, description='', project_id='', state_id='', team_id=''):
        q = """
            mutation IssueCreate {{
              issueCreate(
                input: {{
                    title: "{title}"
                    description: {description}
                    projectId: "{project_id}"
                    stateId: "{state_id}"
                    teamId: "{team_id}"
                }}
              ) {{
                success
                issue {{
                  id
                  title
                }}
              }}
            }}
            """.format(title=title, description=description, project_id=project_id, team_id=team_id, state_id=state_id)
        print(q)
        create_response = self.query_grapql(q)
        return create_response['data']['issueCreate']

    def teams(self):
        return self.query_basic_resource('teams')

    def states(self):
        return self.query_basic_resource('workflowStates')

    def projects(self):
        return self.query_basic_resource('projects')

    def get_issue(self, id):
        return self.query_grapql("""
            query Q {{
                issue(
                    id: "{id}"
                ){{
                    id,
                    number,
                    url
                }}
            }}
        """.format(id=id))

