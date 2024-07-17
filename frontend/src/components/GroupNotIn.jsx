import React, { useState, useEffect } from 'react';

const GroupNotIn = () => {
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    // Fetch available groups
    const fetchGroups = async () => {
      try {
        const response = await fetch('/api/groups', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        setGroups(data.groups);
      } catch (error) {
        console.error('Error fetching groups:', error);
      }
    };
    fetchGroups();
  }, []);

  const handleJoinGroup = async (groupId) => {
    // Handle join group request
  };

  const handleCreateGroup = () => {
    // Handle create group
  };

  return (
    <div className="group-not-in">
      <h2>You are not in a group</h2>
      <button onClick={handleCreateGroup}>Create</button>
      <h3>Groups</h3>
      {groups.map((group) => (
        <div key={group.id} className="group-item">
          <span>{group.name}</span>
          <span>{group.members.length}/{group.maxMembers}</span>
          <span>{group.owner}</span>
          <button onClick={() => handleJoinGroup(group.id)}>Send request</button>
        </div>
      ))}
    </div>
  );
};

export default GroupNotIn;
