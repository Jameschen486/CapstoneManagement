import React, { useState } from 'react';
import GroupRequests from './GroupRequests';

const GroupIn = ({ groupData }) => {
  const [showRequests, setShowRequests] = useState(false);

  const handleLeaveGroup = async () => {
    const userId = localStorage.getItem('userId');
    const token = localStorage.getItem('token');
    
    try {
      const formData = new FormData();
      formData.append('userid', userId);

      const response = await fetch('http://localhost:5001/group/leave', {
        method: 'POST',
        body: formData,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message);
        window.location.reload(); // Reload the page
      } else {
        alert(data.description || 'An error occurred');
      }
    } catch (error) {
      console.error('Error leaving group:', error);
      alert('An error occurred. Please try again.');
    }
  };

  return (
    <div className="group-in">
      <h2>Group: {groupData.groupname}</h2>
      <h3>Members:</h3>
      {groupData.group_members.map((member) => (
        <div key={member.userid} className="member-item">
          <span>{member.firstname} {member.lastname}</span>
        </div>
      ))}
      <button onClick={handleLeaveGroup}>Leave group</button>
      {groupData.ownerid === parseInt(localStorage.getItem('userId'), 10) && (
        <>
          <button onClick={() => setShowRequests(!showRequests)}>View Requests</button>
          {showRequests && <GroupRequests groupId={groupData.groupid} />}
        </>
      )}
    </div>
  );
};

export default GroupIn;
