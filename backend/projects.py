
from typing import Union
from error import InputError, AccessError, RoleError
from werkzeug.datastructures import ImmutableMultiDict
import dbAcc, permission, load
from authentication import return_user
import typing

class Project:
    pass

class Project:
    def __init__(self, 
                 projectid:int, 
                 ownerid:int,
                 title:str, 
                 clients:str = None,    
                 specializations:str = None,  
                 groupcount:int = 0,
                 background:str = None, 
                 requirements:str = None, 
                 reqknowledge:str = None, 
                 outcomes:str = None, 
                 supervision:str = None,
                 additional:str = None,
                 channel:Union[int, None] = None,
                ):
        
        '''
        This constructor is treated as private
        '''
        
        self.projectid = projectid
        self.ownerid = ownerid
        self.title = title
        self.clients = clients
        self.specializations = specializations
        self.groupcount = groupcount
        self.background = background
        self.requirements = requirements
        self.reqknowledge = reqknowledge
        self.outcomes = outcomes
        self.supervision = supervision
        self.additional = additional
        self.channel = channel


    def title_is_valid(title:str) -> bool:
        return title is not None


    def title_exist(title:str) -> bool:
        projects_list = Project.load_all().values()
        titles_list = [p.title for p in projects_list]
        return title in titles_list
        

    def create(userid:int, ownerid:int, title:str):
        '''
        create a project in database
        '''
        load.user(ownerid)
        permission.project_create(userid, ownerid)

        if not Project.title_is_valid(title):
            raise InputError(description=f"Invalid project title: {title}")
        if Project.title_exist(title):
            raise InputError(description="Project with the same title already exists")

        dummy_project_info = vars(Project(None, ownerid, title))
        dummy_project_info.pop("projectid")
        dummy_project_info.pop("channel")

        projectid = dbAcc.create_project(*dummy_project_info.values())

        return {"message": "Project created.", "projectid": projectid}, 201
       

    def get_details(userid: int, projectid: int):
        project = load.project(projectid)
        permission.project_details(userid, projectid)

        response = vars(Project(*project))
        return response, 200
    

    def view_all(userid: int) -> typing.Dict[int, Project]:
        '''
        View all projects. Client only see his projects
        '''
        permission.projects_view_all(userid)

        projects = Project.load_all()

        user = return_user(userid)
        if user["role"] == permission.Role.CLIENT:
            projects = {k: v for k, v in projects.items() if v.ownerid == userid}

        projects = {k: vars(v) for k, v in projects.items()}
        return projects, 200


    def load_all() -> typing.Dict[int, Project]:
        '''
        Load all projects from database
        '''
        projects_info = dbAcc.get_all_projects()
        projects = dict()
        for project_info in projects_info:
            project = Project(*project_info)
            projects[project.projectid] = project

        return projects


    def update(data:ImmutableMultiDict):
        '''
        Update a project in database.
        This is done by creating a new project with the same id.
        '''
       
        userid = int(data['userid'])
        projectid = data.get('projectid', default=None, type=int)
        title = data.get('title', default=None)
        old_project = Project(*load.project(projectid))

        permission.project_edit(userid, projectid)

        if Project.title_exist(title):
            # Also, new title can't be identical to the original title
            raise InputError(description=f"Project with title {title} exists")
        
        if title == None:
            title = old_project.title

        new_project = Project(
            projectid,
            data.get('ownerid', default=old_project.ownerid),
            title,
            clients=data.get('clients', default=old_project.clients),
            specializations=data.get('specializations', default=old_project.specializations),
            groupcount=data.get('groupcount', default=old_project.groupcount, type=int),
            background=data.get('background', default=old_project.background),
            requirements=data.get('requirements', default=old_project.requirements),
            reqknowledge=data.get('reqknowledge', default=old_project.reqknowledge),
            outcomes=data.get('outcomes', default=old_project.outcomes),
            supervision=data.get('supervision', default=old_project.supervision),
            additional=data.get('additional', default=old_project.additional),
            channel=data.get('channel', default=old_project.channel, type=int),
        )


        new_project_info = vars(new_project)
        new_project_info.pop('channel')
        dbAcc.update_project(*new_project_info.values())

        return {"message": "Project updated.", "projectid": projectid}, 200


    def delete(userid:int, projectid:int):
        load.project(projectid)
        permission.project_edit(userid, projectid)

        dbAcc.delete_project_by_id(projectid)

        return {"message": "Project deleted.", "projectid": projectid}, 200




