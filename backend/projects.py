
from typing import Union
from error import InputError, AccessError
from werkzeug.datastructures import ImmutableMultiDict
import dbAcc

class Project:
    pass

class Project:
    def __init__(self, 
                 project_id:int, 
                 owner_id:int,
                 title:str, 
                 clients:str = None,    
                 specializations:str = None,  
                 group_count:Union[int, None] = None,
                 background:str = None, 
                 requirements:str = None, 
                 req_knowledge:str = None, 
                 outcomes:str = None, 
                 supervision:str = None,
                 additional:str = None,
                 channel:Union[int, None] = None,
                 ):
        
        '''
        This constructor is treated as private
        '''
        
        self.project_id = project_id
        self.owner_id = owner_id
        self.title = title
        self.clients = clients
        self.specializations = specializations
        self.group_count = group_count
        self.background = background
        self.requirements = requirements
        self.req_knowledge = req_knowledge
        self.outcomes = outcomes
        self.supervision = supervision
        self.additional = additional
        self.channel = channel



    def title_is_valid(title:str) -> bool:
        return title != None


    def title_exist(title:str) -> bool:
        projects_list = Project.load_all().values()
        titles_list = [p.title for p in projects_list]
        return title in titles_list
        

    def create(title:str, owner_id:int):
        '''
        create a project in database
        '''
        if not Project.title_is_valid(title):
            raise InputError(description=f"Invalid project title: {title}")
        if Project.title_exist(title):
            raise InputError(description="Project with the same title already exists")

        dummy_project_info = vars(Project(None, owner_id, title))
        dummy_project_info.pop("project_id")
        dummy_project_info.pop("channel")

        project_id = dbAcc.create_project(*dummy_project_info.values())

        return {"message": "Project created.", "project_id": project_id}, 201
       

    def get_details(project_id: int, user_id: int):
        project = Project.load(project_id)
        if (project == None):
            raise InputError(description=f"Project with id {project_id} does not exist")
        if user_id != project.owner_id:
            # Tutor might be allowed to get details of other projects
            raise AccessError(description=f"Project with id {project_id} is not your project.")

        response = vars(project)
        return response, 201


    def load(project_id:int) -> Project:
        '''
        Load a project from database
        '''
        if (project_id == None):
            return None
        
        project_info = dbAcc.get_project_by_id(project_id)
        project = Project(*project_info) if (project_info != None) else None
        return project
    

    def load_all() -> dict:
        '''
        Load all projects from database
        '''
        projects_info = dbAcc.get_all_projects()
        projects = dict()
        for project_info in projects_info:
            project = Project(*project_info)
            projects[project.project_id] = project

        return projects


    def update(data:ImmutableMultiDict):
        '''
        Update a project in database.
        This is done by creating a new project with the same id.
        '''
       
        user_id = int(data['user_id'])
        project_id = data.get('project_id', default=None, type=int)
        title = data.get('title', default=None)
        old_project = Project.load(project_id)

        # Check 1: existence of the project
        if old_project == None:
            raise InputError(description=f"Project with id {project_id} does not exist")
        # Check 2: premission of updating the project
        if user_id != old_project.owner_id:
            # Tutor might be allowed to update other projects
            raise AccessError(description=f"Project with id {project_id} is not your project.")
        # Check 3: no duplicate title
        if title != None and Project.title_exist(title):
            # Also, new title can't be identical to the original title
            raise InputError(description=f"Project with title {title} exists")

        new_project = Project(
            project_id,
            user_id,
            title,
            clients=data.get('clients', default=old_project.clients),
            specializations=data.get('specializations', default=old_project.specializations),
            group_count=data.get('group_count', default=old_project.group_count, type=int),
            background=data.get('background', default=old_project.background),
            requirements=data.get('requirements', default=old_project.requirements),
            req_knowledge=data.get('req_knowledge', default=old_project.req_knowledge),
            outcomes=data.get('outcomes', default=old_project.outcomes),
            supervision=data.get('supervision', default=old_project.supervision),
            additional=data.get('additional', default=old_project.additional),
            channel=data.get('channel', default=old_project.channel, type=int),
        )


        new_project_info = vars(new_project)
        new_project_info.pop('channel')
        dbAcc.update_project(*new_project_info.values())

        return {"message": "Project updated.", "project_id": project_id}, 201


    def delete(user_id:int, project_id:int):
        project = Project.load(project_id)
        if (project == None):
            raise InputError(description=f"Project with id {project_id} does not exist")
        if (project.owner_id != user_id):
            # Tutor might be allowed to update other projects
            raise AccessError(description=f"Project with id {project_id} is not your project")
        
        dbAcc.delete_project_by_id(project_id)
        #print("calling dbAcc.create_project() with arguements: ", end="")
        #print(project_id)

        return {"message": "Project deleted.", "project_id": project_id}, 201




