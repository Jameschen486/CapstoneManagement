
from backend.error import InputError, AccessError
from werkzeug.datastructures import ImmutableMultiDict
from backend import dbAcc

class Project:
    pass

class Project:
    def __init__(self, 
                 project_id:int, 
                 name:str,
                 owner_id:int,   
                 channel_id:int|None = None,    
                 group_id:int|None = None,       
                 spec:str = None, 
                 description:str = None, 
                 requirement:str = None, 
                 required_knowledge:str = None, 
                 outcome:str = None, 
                 additional:str = None,
                 ):
        '''
        This constructor is treated as private
        '''
        
        self.project_id = project_id
        self.name = name
        self.owner_id = owner_id
        self.channel_id = channel_id
        self.group_id = group_id
        self.spec = spec
        self.description = description
        self.requirement = requirement
        self.required_knowledge = required_knowledge
        self.outcome = outcome
        self.additional = additional


    def name_is_valid(name:str) -> bool:
        return name != None


    def name_exist(name:str) -> bool:
        projects_list = Project.load_all().values()
        names_list = [p.name for p in projects_list]
        return name in names_list
        

    def create(name:str, owner_id:int):
        '''
        create a project in database
        '''
        if not Project.name_is_valid(name):
            raise InputError(description=f"Invalid project name: {name}")
        if Project.name_exist(name):
            raise InputError(description="Project with the same name already exists")

        dummy_project = Project(None, name, owner_id)
        vars(dummy_project).pop("project_id")

        #project_id = dbAcc.create_project(*vars(dummy_project).values())
        print("calling dbAcc.create_project() with arguements: ", end="")
        print(*vars(dummy_project).values(), sep=',')
        project_id = 0
        #

        return {"message": "Project created.", "project_id": project_id}, 201
       

    def load(project_id:int) -> Project:
        '''
        Load a project from database
        '''
        #project_info = dbAcc.get_project_by_id(project_id)
        project_info = [0, "name", 1, 2, 3, "spec", "description", 
             "requirement", "required_knowledge", "outcome", "additional"]
        #

        return Project(*project_info)
    

    def load_all() -> dict[int, Project]:
        '''
        Load all projects from database
        '''
        #projects_info = dbAcc.get_all_projects()
        projects_info = []
        projects = dict[int, Project]()
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
        project_id = int(data['project_id'])
        name = data.get('name')
        old_project = Project.load(project_id)

        # Check 1: existence of the project
        if old_project == None:
            raise InputError(description=f"Project with id {project_id} does not exist")
        # Check 2: premission of updating the project
        if user_id != old_project.owner_id:
            # Tutor might be allowed to update other projects
            raise AccessError(description=f"Project with id {project_id} is not your project")
        # Check 3: no duplicate name
        if name != None and Project.name_exist(name):
            # Also, new name can't be identical to the original name
            raise InputError(description=f"Project with name {name} exists")

        new_project = Project(
            project_id,
            name,
            user_id,
            group_id=data.get('group_id', default=old_project.group_id, type=int),
            spec=data.get('spec', default=old_project.spec),
            description=data.get('description', default=old_project.description),
            requirement=data.get('requirement', default=old_project.requirement),
            required_knowledge=data.get('required_knowledge', default=old_project.required_knowledge),
            outcome=data.get('outcome', default=old_project.outcome),
            additional=data.get('additional', default=old_project.additional), 
        )

        #dbAcc.update_project(*vars(new_project).values())
        print("calling dbAcc.update_project() with arguements: ", end="")
        print(*vars(new_project).values(), sep=',')
        #

        return {"message": "Project updated.", "project_id": project_id}, 201










