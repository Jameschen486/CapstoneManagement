import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProjectDetailsModal from './ProjectDetailsModal';
import '../css/Projects.css';

const Projects = () => {
  const [activeContainer, setActiveContainer] = useState('projects');
  const navigate = useNavigate();

  const handleBack = () => {
    navigate('/dashboard'); 
  };

  return (
    <div className='client-page'>
      <header className='client-header'>
        <h1>Client Page</h1>
        <button onClick={handleBack} className="back-button">Back to Dashboard</button>
      </header>
      <div className='client-content'>
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
    <div className='client-skills-container'>
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
      <ul className='client-skills-list'>
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
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('userId');

        const userResponse = await fetch(`http://localhost:5001/user?id=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!userResponse.ok) {
          throw new Error('Failed to fetch user data');
        }

        const userData = await userResponse.json();
        console.log('User data:', userData);

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
        console.log('Projects array:', projectsArray);
        setProjects(projectsArray);

      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Error fetching data');
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
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

  return (
    <div className="projects-container">
      <div className="projects-content">
        {loading && <p>Loading projects...</p>}
        {error && <p>Error: {error}</p>}
        {!loading && !error && projects.length === 0 && <p>No projects available.</p>}
        <h2 className='NumofProjects'>Number of projects: {projects.length}</h2>
        {!loading && !error && projects.length > 0 && (
          <ul>
            {projects.map(project => (
            <li key={project.projectid} onClick={() => handleProjectClick(project.projectid)}>
                <div className='project-title'>{project.title}</div>
            </li>
            ))}
          </ul>
        )}
        <button onClick={handleCreateProject} className="create-project-button">Create New Project</button>
      </div>
      {selectedProjectId && (
        <ProjectDetailsModal projectId={selectedProjectId} onClose={handleCloseModal} />
      )}
    </div>
  );
};

export default Projects;
