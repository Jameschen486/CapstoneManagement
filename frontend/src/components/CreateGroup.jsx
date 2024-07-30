import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/CreateGroup.css'

const CreateGroup = () => {
  const [groupName, setGroupName] = useState('');
  const navigate = useNavigate();

  const handleCreateGroup = async () => {
    try {
      const formData = new FormData();
      formData.append('groupname', groupName);
      formData.append('ownerid', localStorage.getItem('userId'));

      const response = await fetch('http://localhost:5001/group/create', {
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

      const data = JSON.parse(text);
      alert('Group created successfully!');
      setTimeout(() => {
        navigate('/groups');
      }, 2000);  // Redirect after 2 seconds
    } catch (error) {
      console.error('Error creating group:', error);
      alert(error.message);
    }
  };

  const handleBack = () => {
    navigate('/groups');
  };

  return (
    <div className='create-group-container'>
      <header className='create-group-header'>
        <h1>Create Group</h1>
        <button onClick={handleBack} className="back-button">Back to Groups</button>
      </header>
      <div className='content'>
        <p>Enter Group Name:</p>
        <input
          className='group-name-input'
          type="text"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
          placeholder="Group Name"
        />
        <button onClick={handleCreateGroup} className='create-group-button'>Create Group</button>
      </div>
    </div>
  );
};

export default CreateGroup;
