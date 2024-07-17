import React, { useState } from 'react';
import GroupRequests from './GroupRequests';

const GroupIn = ({ groupData }) => {
  const [showRequests, setShowRequests] = useState(false);

  const handleLeaveGroup = async () => {
    // Handle leave group request
  };

  return (
    <div className="group-in">
      <h2>Group: {groupData.groupname}</h2>
      <h3>Members:</h3>
      {groupData.group_members.map((member) => (
        <div key={member.userid} className="member-item">
          <span>{member.first_name} {member.last_name}</span>
        </div>
      ))}
      <button onClick={handleLeaveGroup}>Leave group</button>
      {groupData.isOwner && (
        <>
          <button onClick={() => setShowRequests(!showRequests)}>View Requests</button>
          {showRequests && <GroupRequests />}
        </>
      )}
    </div>
  );
};

export default GroupIn;
