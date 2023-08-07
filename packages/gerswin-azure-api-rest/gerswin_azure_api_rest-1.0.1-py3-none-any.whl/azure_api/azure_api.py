import json
import urllib

import requests
from requests.auth import HTTPBasicAuth


class AzureDevOpsAPI:
    def __init__(self, organization, project, team, access_token):
        self.organization = organization
        self.team = team
        self.project = project
        self.access_token = access_token
        self.api_version = "api-version=6.0-preview.3"
        self.auth_header = HTTPBasicAuth("", self.access_token)
        self.base_url_ = f"https://dev.azure.com/{self.organization}"
        self.base_url = f"https://dev.azure.com/{self.organization}/{urllib.request.pathname2url(self.project)}"
        self.headers = {
            "Content-Type": "application/json"
        }

    def query_iterations(self, timeframe):
        url = f"{self.base_url}/_apis/work/teamsettings/iterations?$timeframe={timeframe}&{self.api_version}"
        response = requests.get(url, headers=self.headers, auth=self.auth_header)
        response_json = json.loads(response.text)
        response.raise_for_status()
        return response_json["value"]

    def get_items_by_wiql(self, wiql):
        url = f"https://dev.azure.com/{self.organization}/{self.project}/{self.team}/_apis/wit/wiql?api-version=7.0"
        payload = {"query": wiql}
        response = requests.post(url, auth=self.auth_header, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_work_items_id(self, wiql):
        response_json = self.get_items_by_wiql(wiql)
        return [work_item["id"] for work_item in response_json["workItems"]]

    def get_work_items_by_wiql(self, wiql):
        ids = self.get_work_items_id(wiql)
        url = f"{self.base_url}/_apis/wit/workitems?ids={','.join(map(str, ids))}&{self.api_version}"
        response = requests.get(url, auth=self.auth_header)
        response.raise_for_status()
        return response.json()

    def get_work_items_by_ids(self, ids):
        url = f"{self.base_url}/_apis/wit/workitems?ids={','.join(map(str, ids))}&{self.api_version}"
        response = requests.get(url, auth=self.auth_header)
        return response.json()

    def update_work_item(self, field, task_id, value):
        payload = [
            {
                'op': 'add',
                'path': f'/fields/{field}',
                'value': value
            }
        ]
        url = f"{self.base_url}/_apis/wit/workitems/{task_id}?{self.api_version}"
        headers = {
            "Content-Type": "application/json-patch+json"
        }
        return requests.patch(
            url=url,
            json=payload,
            headers=headers,
            auth=self.auth_header
        )

    def list_projects(self):
        url = f"{self.base_url_}/_apis/projects?{self.api_version}"
        response = requests.get(
            url=url,
            headers=self.headers,
            auth=self.auth_header
        )
        response.raise_for_status()
        return response

    def list_teams(self):
        url = f"{self.base_url_}/_apis/projects/{self.project}/teams?{self.api_version}"
        response = requests.get(
            url=url,
            headers=self.headers,
            auth=self.auth_header
        )
        response.raise_for_status()
        return response

    def get_current_iteration(self):
        url = f"{self.base_url}/_apis/work/teamsettings/iterations?team={self.team}&project={self.project}&{self.api_version}"
        response = requests.get(
            url=url,
            headers=self.headers,
            auth=self.auth_header
        )
        response.raise_for_status()
        return response

    def add_comment_to_work_item(self, work_item_id, comment):
        url = f"{self.base_url}/_apis/wit/workItems/{work_item_id}/comments?{self.api_version}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "text": comment
        }
        return requests.post(
            url=url,
            json=payload,
            headers=headers,
            auth=self.auth_header
        ).json()

    def get_user_info(self, email):
        url = f"https://vsaex.dev.azure.com/Linktic/_apis/userentitlements?$filter=name eq '{email}'&api-version=7.0"
        response = requests.get(
            url=url,
            headers=self.headers,
            auth=self.auth_header
        )
        response.raise_for_status()
        return response
