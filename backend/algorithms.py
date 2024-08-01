import numpy as np
import dbAcc
import sys
from scipy.optimize import linear_sum_assignment

groups = [{"id" : 1, "skills" : {'python': 2, 'frontend': 1}, "pref": {'1': 3, '2': 2, '3': 1}},
          {"id" : 2, "skills" : {'python' : 3, 'backend': 1}, "pref": {'4': 3, '2': 2, '1': 1}},
          {"id" : 3, "skills" : {'c': 1, 'java': 1, 'python': 1, 'frontend': 1}, "pref": {'5': 3, '4': 2, '2': 1}},
          {"id" : 4, "skills" : {'frontend': 2, 'backend': 1, 'python': 1}, "pref": {'2': 3, '3': 2, '1': 1}}]

projects = [{"id" : 1, "skills" : ['python', 'frontend']},
            {"id" : 2, "skills" : ['c', 'frontend']},
            {"id" : 3, "skills" : ['python', 'backend']},
            {"id" : 4, "skills" : ['java', 'frontend', 'backend']},
            {"id" : 5, "skills" : ['python']}]

# matrix = np.zeros((max(len(groups),len(projects)),max(len(groups),len(projects))))

def main(groups, projects):
    output = []
    matrix = np.zeros((len(groups),len(projects)))

    for i, group in enumerate(groups):
        for j, project in enumerate(projects):
            score = 0
            for skill, value in group['skills'].items():
                if skill in project['skills']:
                    score+= value
            for pref, value in group['pref'].items():
                if int(pref) == project['id']:
                    score+= value
            matrix[i][j] = score
            # print(group['id'], project['id'], score)

    print(matrix, file=sys.stderr)
    row_ind, col_ind = linear_sum_assignment(matrix, maximize = True)
    # print(col_ind)
    # print(row_ind)

    print(matrix[row_ind, col_ind].sum(), file=sys.stderr)

    for i, entry in enumerate(row_ind):
        output.append({'group_id':groups[entry]['id'],'project_id':projects[col_ind[i]]['id']})
        # print(groups[entry]['id'], projects[col_ind[i]]['id'])
    return output

def allocate():
    # print(dbAcc.get_all_preferences(), file=sys.stderr)
    # print(dbAcc.get_all_groups_skills(),  file=sys.stderr)
    groups = []
    projects = []
    max_rank = 3
    for entry in dbAcc.get_all_preferences():
        if entry is None:
            return (None)
        groupid = int(entry[0])
        if groupid not in [group['id'] for group in groups]:
            groups.append({'id': groupid, 'skills': {}, 'pref': {}})

        for group in groups:
            if group['id'] == groupid:
                if entry[1] not in group['pref']:
                    group['pref'][entry[1]] = max_rank-entry[2]
                else:
                    group['pref'][entry[1]] += max_rank-entry[2]
    
    for entry in dbAcc.get_all_groups_skills():
        if entry is None:
            return (None)
        groupid = int(entry[0])
        if groupid not in [group['id'] for group in groups]:
            groups.append({'id': groupid, 'skills': {}, 'pref': {}})
            
        for group in groups:
            if group['id'] == groupid:
                group['skills'][entry[1]] = entry[2]
    
    for entry in dbAcc.get_all_project_skills():
        if entry is None:
            return (None)
        projid = int(entry[0])
        if projid not in [proj['id'] for proj in projects]:
            projects.append({'id':projid,'skills':[]})

        for project in projects:
            if project['id'] == projid:
                project['skills'].append(entry[2])
    print('groups', file=sys.stderr)
    print(groups, file=sys.stderr)
    print('projects', file=sys.stderr)
    print(projects, file=sys.stderr)

    output = main(groups,projects)
    # for group in groups:
    #     group['pref'] = pref_combine(group['pref'])
    return (output)

# def pref_combine(pref, max_rank=3):
#     ranks = {}
#     for entry in pref:
#         if entry[0] not in ranks:
#             ranks[entry[0]] = max_rank-entry[1]
#         else:
#             ranks[entry[0]] += max_rank-entry[1]
#     # ranks = dict(sorted(ranks.items(), key=lambda x: x[1]))
#     return ranks