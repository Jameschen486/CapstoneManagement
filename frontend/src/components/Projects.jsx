import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Projects = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch the group data for the user
    const fetchGroupData = async () => {
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('userId');

        // Fetch user data
        const userResponse = await fetch(`http://localhost:5001/user?id=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const userData = await userResponse.json();
        console.log('User data:', userData);

      } catch (error) {
        console.error('Error fetching group data:', error);
      }
    };
    fetchGroupData();
  }, []);

  const handleCreateProject = () => {
    navigate('/projects/create');
  };

  return (
    <div className="projects-container">
      <header className="projects-header">
        <h1>Projects</h1>
        <button onClick={handleCreateProject} className="create-project-button">Create New Project</button>
      </header>
      <div className="projects-content">
        {loading && <p>Loading projects...</p>}
        {error && <p>Error: {error}</p>}
        {!loading && !error && projects.length === 0 && <p>No projects available.</p>}
        {!loading && !error && projects.length > 0 && (
          <ul>
            {projects.map(project => (
              <li key={project.projectid}>{project.title}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Projects;
