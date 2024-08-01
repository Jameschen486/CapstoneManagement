import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/CreateProject.css';

const CreateProject = () => {
  const [title, setTitle] = useState('');
  const [ownerId, setOwnerId] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleCreateProject = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('userId');

    const formData = new FormData();
    formData.append('userid', userId);
    formData.append('ownerid', userId); // Set ownerid to userid
    formData.append('title', title);

    // Log the form data for debugging
    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }

    try {
      const response = await fetch('http://localhost:5001/project/create', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const responseData = await response.json();
      if (response.ok) {
        setMessage('Project created successfully!');
        setTitle('');
        setTimeout(() => {
            navigate('/projects');
          }, 2000);  // Redirect after 2 seconds

      } else {
        throw new Error(responseData.error || 'Failed to create project');
      }
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className='create-group-container'>
      <div className='create-group-header'>
        <h1>Create Project</h1>
        <button onClick={() => navigate('/projects')} className='create-group-button'>Back</button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <form onSubmit={handleCreateProject} className='content'>
        <input
          className='group-name-input'
          type="text"
          placeholder="Project Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <button type="submit" className='create-group-button'>Create Project</button>
        <p>You can add skills and update project detail after you create the project</p>
      </form>
    </div>
  );
};

export default CreateProject;
