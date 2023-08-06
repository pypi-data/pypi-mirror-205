def get_readme_template(project_name):
    txt = '''\
# momo_PJ_name #
!!project description.

## Maintainer ##
!! your email address.

## Parameters ##
- `!!param`: !!type, default=!!default value. !!explanation

## Input & Output ##
Input:
- `!!file_name`  # !!comments

Output:
```
└── output
    ├── !!file_name_1  # !!comments
    └── !!file_name_2  # !!comments
```
'''
    return txt.replace('momo_PJ_name', project_name)
