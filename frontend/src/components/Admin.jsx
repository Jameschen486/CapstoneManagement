import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProjectDetailsModal from './ProjectDetailsModal';
import '../css/Admin.css';
import '../css/Projects.css';

const AdminPage = () => {
  const [activeContainer, setActiveContainer] = useState('skills');
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/dashboard'); 
  };

  return (
    <div className='admin-page'>
      <header className='admin-header'>
        <h1>Admin Page</h1>
        <button onClick={handleBack} className="back-button">Back to Dashboard</button>
      </header>
      <div className='admin-content'>
        <div className='navigation-arrows'>
          <button onClick={() => setActiveContainer('skills')} className='arrow-button'>Skills</button>
          <button onClick={() => setActiveContainer('projects')} className='arrow-button'>Projects</button>
        </div>
        {activeContainer === 'skills' && <ManageSkills />}
        {activeContainer === 'projects' && <ManageProjects />}
      </div>
    </div>
  );
};

const ManageSkills = () => {
  const [skillName, setSkillName] = useState('');
  const [skills, setSkills] = useState([]);

  const fetchSkills = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/skills/view?userid=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      console.log(data);
      if (response.ok) {
        // Convert the object of skills to an array
        const skillsArray = Object.values(data);
        setSkills(skillsArray);
      } else {
        throw new Error('Failed to load skills');
      }
    } catch (error) {
      console.error('Error fetching skills:', error);
      alert('Error fetching skills');
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleCreateSkill = async () => {
    try {
      const formData = new FormData();
      formData.append('skillname', skillName);
      formData.append('userid', localStorage.getItem('userId'));

      const response = await fetch('http://localhost:5001/skill/create', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: formData,
      });

      const text = await response.text();
      if (!response.ok) {
        console.log('Server response:', text);
        throw new Error(text);
      }

      alert('Skill created successfully!');
      setSkillName(''); // Reset the skill name input
      fetchSkills(); // Fetch skills again to update the list
    } catch (error) {
      console.error('Error creating skill:', error);
      alert(error.message);
    }
  };

  return (
    <div className='admin-skills-container'>
      <h2>Manage Skills</h2>
      <p>Enter Skill Name:</p>
      <input
        className='skill-name-input'
        type="text"
        value={skillName}
        onChange={(e) => setSkillName(e.target.value)}
        placeholder="Skill Name"
      />
      <button onClick={handleCreateSkill} className='create-skill-button'>Create Skill</button>

      <h2 className='skills-list-title'>Skills List</h2>
      <ul className='admin-skills-list'>
        {skills.length > 0 ? (
          skills.map((skill) => (
            <li key={skill.skillid}>{skill.skillname}</li>
          ))
        ) : (
          <li>No skills found</li>
        )}
      </ul>
    </div>
  );
};


const ManageProjects = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [groups, setGroups] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState('');
  const [selectedGroupId, setSelectedGroupId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [assigned, setAssigned] = useState([]);

  useEffect(() => {
    const fetchProjectsAndGroups = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('userId');

        const projectsResponse = await fetch(`http://localhost:5001/projects/view?userid=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!projectsResponse.ok) {
          throw new Error('Failed to fetch projects');
        }

        const projectsData = await projectsResponse.json();
        console.log('Projects data:', projectsData);

        // Convert object to array
        const projectsArray = Object.keys(projectsData).map(key => ({
          projectid: key,
          ...projectsData[key]
        }));
        setProjects(projectsArray);

        const groupsResponse = await fetch(`http://localhost:5001/groups/view?userid=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!groupsResponse.ok) {
          throw new Error('Failed to fetch groups');
        }

        const groupsData = await groupsResponse.json();
        console.log('Groups data:', groupsData);

        // Convert array of arrays to array of objects
        const groupsArray = groupsData.map(group => ({
          groupid: group[0],
          groupname: group[1],
          ownerid: group[2]
        }));
        setGroups(groupsArray);

      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Error fetching data');
      } finally {
        setLoading(false);
      }
    };
    fetchProjectsAndGroups();
  }, []);

  const handleCreateProject = () => {
    navigate('/projects/create');
  };

  const handleProjectClick = (projectId) => {
    setSelectedProjectId(projectId);
  };

  const handleCloseModal = () => {
    setSelectedProjectId(null);
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  const handleAssignProject = async () => {
    if (!selectedProjectId || !selectedGroupId) {
      alert('Please select a project and a group.');
      return;
    }

    try {
      const formData = new FormData();
      formData.append('groupid', selectedGroupId);
      formData.append('projectid', selectedProjectId);

      const response = await fetch('http://localhost:5001/group/assign_project', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: formData,
      });

      const text = await response.text();
      if (!response.ok) {
        console.log('Server response:', text);
        throw new Error(text);
      }

      alert('Project assigned successfully!');
    } catch (error) {
      console.error('Error assigning project:', error);
      alert(error.message);
    }
  };

  const handleAuto = async () => {
    const response = await fetch('http://localhost:5001/allocate/auto', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    const data = await response.json();
    console.log(data);
    setAssigned(data);
  }

  const handleUnAuto = async () => {
    const response = await fetch('http://localhost:5001/unallocate/auto', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    const data = await response;
  }

  return (
    <div className="projects-container">
      <div className="groups-content">
        <h2>Assign Project to Group</h2>
        <select onChange={(e) => setSelectedProjectId(e.target.value)} value={selectedProjectId || ''}>
          <option value="" disabled>Select a project</option>
          {projects.map(project => (
            <option key={project.projectid} value={project.projectid}>{project.title}</option>
          ))}
        </select>
        <select onChange={(e) => setSelectedGroupId(e.target.value)} value={selectedGroupId || ''}>
          <option value="" disabled>Select a group</option>
          {groups.map(group => (
            <option key={group.groupid} value={group.groupid}>{group.groupname}</option>
          ))}
        </select>
        <button onClick={handleAssignProject} className="assign-project-button">Assign Project</button>
        <button onClick={handleAuto} className="assign-project-button">Auto Assign All Projects</button>
        <button onClick={handleUnAuto} className="assign-project-button">Auto Unassign All Project</button>
        {assigned ? (<>{assigned.map(data => (<p>group: {data.group_id} matched with project: {data.project_id}</p>))}</>):(<></>)}
      </div>
    </div>
  );
};

export default AdminPage;
