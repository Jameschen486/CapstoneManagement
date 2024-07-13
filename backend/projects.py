
from typing import Union
from error import InputError, AccessError
from werkzeug.datastructures import ImmutableMultiDict
import dbAcc, premission

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

        if dbAcc.get_user_by_id(ownerid) is None:
            raise InputError(description=f"Intended owner {ownerid} does not exist")

        if not premission.project_create(userid, ownerid):
            return

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
        project = Project.load(projectid)
        if (project is None):
            raise InputError(description=f"Project with id {projectid} does not exist")
    
        if not premission.project_details(userid, projectid):
            return

        response = vars(project)
        return response, 200


    def load(projectid:int) -> Project:
        '''
        Load a project from database
        '''
        if (projectid is None):
            return None
        
        project_info = dbAcc.get_project_by_id(projectid)
        project = Project(*project_info) if (project_info is not None) else None
        return project
    

    def load_all() -> dict:
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
        old_project = Project.load(projectid)


        if old_project is None:
            raise InputError(description=f"Project with id {projectid} does not exist")

        if not premission.project_update(userid, projectid):
            return
        
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
        project = Project.load(projectid)
        if (project is None):
            raise InputError(description=f"Project with id {projectid} does not exist")
        
        if not premission.project_delete(userid, projectid):
            return
        
        dbAcc.delete_project_by_id(projectid)

        return {"message": "Project deleted.", "projectid": projectid}, 200




