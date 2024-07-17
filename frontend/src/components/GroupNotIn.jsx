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
        setGroups(data);
      } catch (error) {
        console.error('Error fetching groups:', error);
      }
    };
    fetchGroups();
  }, []);

  const handleJoinGroup = async (groupId) => {
    try {
      const response = await fetch('http://localhost:5001/group/join', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          groupid: groupId,
          userid: localStorage.getItem('userid'),
        }),
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
          <span>{group.ownerid}</span>
          <button onClick={() => handleJoinGroup(group.groupid)}>Send request</button>
        </div>
      ))}
    </div>
  );
};

export default GroupNotIn;
