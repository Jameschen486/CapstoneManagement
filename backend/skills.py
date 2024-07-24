from typing import Union
from error import InputError, AccessError, RoleError
from werkzeug.datastructures import ImmutableMultiDict
import dbAcc, permission, load
import typing

class Skill:
    pass

class Skill:
    def __init__(self, 
                 skillid:int, 
                 skillname:str, 
                ):
        
        '''
        This constructor is treated as private
        '''
        
        self.skillid = skillid
        self.skillname = skillname

    def name_is_valid(name:str) -> bool:
        return name is not None


    def name_exist(name:str) -> bool:
        skills = Skill.load_all()
        titles_list = [p.skillname for p in skills.values()]
        return name in titles_list


    def create(userid:int, skillname:str):
        '''
        create a skill in database
        '''
        permission.skill_create(userid)

        if not Skill.name_is_valid(skillname):
            raise InputError(description=f"Invalid skill name: {skillname}")
        if Skill.name_exist(skillname):
            raise InputError(description="Skill with the same name already exists")

        dummy_skill_info = vars(Skill(None, skillname))
        dummy_skill_info.pop("skillid")


        skillid = dbAcc.create_skill(*dummy_skill_info.values())

        return {"message": "Skill created.", "skillid": skillid}, 201
       

    def view(userid: int) -> typing.Dict[int, Skill]:
        '''
        View all skills
        '''
        permission.skill_view()

        skills = Skill.load_all()

        skills = {k: vars(v) for k, v in skills.items()}
        return skills, 200
    

    def load_all() -> typing.Dict[int, Skill]:
        '''
        Load all skills from database
        '''
        skills_info = dbAcc.get_all_skills()
        skills = dict()
        for skill_info in skills_info:
            skill = Skill(*skill_info)
            skills[skill.skillid] = skill

        return skills
    

    """
    We might also want:
    def get_details(userid:int, skillid: int)
    def delete(userid:int, skillid: int)
    def update(userid:int, skillid:int, skillname:str)
    """

    def add_skill_student(userid:int, studentid:int, skillid:int):
        load.user(studentid)
        load.skill(skillid)
        permission.skill_set_student(userid, studentid)

        if skillid in dbAcc.get_user_skills(userid):
            raise InputError(description=f"Student {studentid} already has skill {skillid}")
        
        dbAcc.add_skill_to_user(skillid, userid)

        return {"message": "Skill added.", "studentid": studentid, "skillid":skillid}, 201


    def view_skills_student(userid:int, studentid:int):
        load.user(userid)
        load.user(studentid)
        permission.skill_view_student(studentid)

        skill_ids = dbAcc.get_user_skills(studentid)
        skills = Skill.load_all()
        student_skills = {id: skills[id].skillname for id in skill_ids}

        return student_skills, 200


    def remove_skill_student(userid:int, studentid:int, skillid:int):
        load.user(studentid)
        load.skill(skillid)
        permission.skill_set_student(userid, studentid)

        if skillid not in dbAcc.get_user_skills(userid):
            raise InputError(description=f"Student {studentid} does not have skill {skillid}")
        
        dbAcc.remove_skill_from_user(skillid, userid)

        return {"message": "Skill removed.", "studentid": studentid, "skillid":skillid}, 200


    def add_skill_project(userid:int, projectid:int, skillid:int):
        load.project(projectid)
        load.skill(skillid)
        permission.skill_set_project(userid, projectid)

        if skillid in [skill.skill_id for skill in dbAcc.get_project_skills(projectid)]:
            raise InputError(description=f"Project {projectid} already has skill {skillid}")
        
        dbAcc.add_skill_to_project(skillid, projectid)

        return {"message": "Skill added.", "projectid": projectid, "skillid":skillid}, 201


    def view_skills_project(userid:int, projectid:int):
        load.user(userid)
        load.project(projectid)
        permission.skill_view_project()

        skill_ids = [s.skill_id for s in dbAcc.get_project_skills(projectid)] 
        skills = Skill.load_all()
        project_skills = {id: skills[id].skillname for id in skill_ids}

        return project_skills, 200


    def remove_skill_project(userid:int, projectid:int, skillid:int):
        load.project(projectid)
        load.skill(skillid)
        permission.skill_set_project(userid, projectid)

        if skillid not in [skill.skill_id for skill in dbAcc.get_project_skills(projectid)]:
            raise InputError(description=f"Project {projectid} does not have skill {skillid}")
        
        dbAcc.remove_skill_from_project(skillid, projectid)

        return {"message": "Skill removed.", "projectid": projectid, "skillid":skillid}, 200




