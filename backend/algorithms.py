import numpy as np
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

print(matrix)
row_ind, col_ind = linear_sum_assignment(matrix, maximize = True)
# print(col_ind)
# print(row_ind)

print(matrix[row_ind, col_ind].sum())

for i, entry in enumerate(row_ind):
    print(groups[entry]['id'], projects[col_ind[i]]['id'])
