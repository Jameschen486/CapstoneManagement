import React, { useState, useEffect } from 'react';
import GroupRequests from './GroupRequests';
import {ChatBox, ProjectBox} from './utils';

const GroupIn = ({ groupData }) => {
  const [showRequests, setShowRequests] = useState(false);
  const [channelId, setChannelId] = useState('');
  const [loaded, setloaded] = useState(false);
  const userId = localStorage.getItem('userId');
  const token = localStorage.getItem('token');
  
  useEffect(() => { 
    findChannel();
  }, []);

  const handleLeaveGroup = async () => {
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

  const findChannel = async () => {
    const response = await fetch(`http://localhost:5001/group/channel?userid=${userId}&groupid=${groupData.groupid}`, {
      method: 'GET',
      headers: {Authorization: `Bearer ${token}`}
    });
    const output = await response.json();
    setChannelId(output.channelid)
  }
  console.log('channelid', channelId)

 
  return (
    <div className="group-in">
      <div style={{display: 'flex'}}>
        <div style={{flexGrow: '1'}}>
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
        <div style={{flexGrow: '1'}}>
          <ProjectBox project={groupData.project} userid={userId} token={token}/>
        </div>
      </div>
      <h3>Chat:</h3>
      <div>
        {channelId ? (
          <>
            <ChatBox userid={userId} channelid={channelId} token={token}/>
          </>
        ) : (
          <>
          </>
        )}
      </div>
    </div>
  );
};

export default GroupIn;
