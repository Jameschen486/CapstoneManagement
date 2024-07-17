import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const MAX_STUDENT_PER_GROUP = 6;

const GroupNotIn = () => {
  const [groups, setGroups] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch available groups
    const fetchGroups = async () => {
      try {
        const response = await fetch('http://localhost:5001/groups/view', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        // Convert the list of tuples to list of objects
        const formattedData = data.map(group => ({
          groupid: group[0],
          groupname: group[1],
          member_count: group[2]
        }));
        setGroups(formattedData);
      } catch (error) {
        console.error('Error fetching groups:', error);
      }
    };
    fetchGroups();
  }, []);

  const handleJoinGroup = async (groupId) => {
    try {
      const formData = new FormData();
      formData.append('groupid', groupId);
      formData.append('userid', localStorage.getItem('userId'));
  
      const response = await fetch('http://localhost:5001/group/join', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: formData,
      });
  
      const data = await response.json();
  
      if (response.ok) {
        alert('Join request sent successfully!');
      } else {
        alert(data.description || 'Failed to send join request');
      }
    } catch (err) {
      console.error('Error:', err);
      alert('An error occurred. Please try again.');
    }
  };

  const handleCreateGroup = () => {
    navigate('/create-group');
  };

  return (
    <div className="group-not-in">
      <h2>You are not in a group</h2>
      <button onClick={handleCreateGroup}>Create</button>
      <h3>Groups</h3>
      {groups.map((group) => (
        <div key={group.groupid} className="group-item">
          <span>{group.groupname}</span>
          <span>{group.member_count}/{MAX_STUDENT_PER_GROUP}</span>
          <button onClick={() => handleJoinGroup(group.groupid)}>Send request</button>
        </div>
      ))}
    </div>
  );
};

export default GroupNotIn;
