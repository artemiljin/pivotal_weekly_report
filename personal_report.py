import datetime
import json

from utils import week_range, render, SERVER, get_request


def get_action_types(data):
    """
    Getting actions you're done on this week
    :param data: result of your activity
    :return: list of unique actions
    """
    results = {}
    projects_data = {}
    for modification in data:
        project_version = modification['project']['id']
        if project_version not in projects_data.keys():
            projects_data[project_version] = modification['project']['name']
        action_type = modification['highlight']
        primary_resources = modification['primary_resources'][0]
        message = f"[{primary_resources['url']}] {primary_resources['name']}"
        if project_version in results.keys():
            if action_type in results[project_version].keys():
                results[project_version][action_type].append(message)
            else:
                results[project_version][action_type] = [message]
        else:
            results[project_version] = {action_type: [message]}
    return results, projects_data


start_date, end_date = week_range(datetime.datetime.now() - datetime.timedelta(5))
params = {'occurred_after': start_date, 'occurred_before': end_date}
activity_data = json.loads(get_request(f'{SERVER}/services/v5/my/activity', params=params))
actions, projects = get_action_types(activity_data)
print(render(tpl_path='templates/report.tmpl',
             context={'start_date': start_date.split('T')[0], 'end_date': end_date.split('T')[0],
                      'actions': actions, 'projects': projects}))
