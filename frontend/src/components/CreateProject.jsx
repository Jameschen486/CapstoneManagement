import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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
    formData.append('title', title);
    if (ownerId) {
      formData.append('ownerid', ownerId);
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
        setOwnerId('');
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
    <div>
      <h1>Create Project</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <form onSubmit={handleCreateProject}>
        <input
          type="text"
          placeholder="Project Title"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Owner ID (optional)"
          value={ownerId}
          onChange={e => setOwnerId(e.target.value)}
        />
        <button type="submit">Create Project</button>
      </form>
    </div>
  );
};

export default CreateProject;
