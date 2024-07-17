import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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
        navigate('/dashboard');
      }, 2000);  // Redirect after 2 seconds
    } catch (error) {
      console.error('Error creating group:', error);
      alert(error.message);
    }
  };

  return (
    <div>
      <h1>Create Group</h1>
      <input
        type="text"
        value={groupName}
        onChange={(e) => setGroupName(e.target.value)}
        placeholder="Group Name"
      />
      <button onClick={handleCreateGroup}>Create Group</button>
    </div>
  );
};

export default CreateGroup;
