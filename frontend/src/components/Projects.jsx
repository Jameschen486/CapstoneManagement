import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProjectDetailsModal from './ProjectDetailsModal';
import '../css/Projects.css';

const Projects = () => {
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

  return (
    <div className="projects-container">
      <header className="projects-header">
        <h1>Your Projects</h1>
      </header>
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
