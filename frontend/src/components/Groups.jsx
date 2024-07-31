import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GroupNotIn from './GroupNotIn';
import GroupIn from './GroupIn';
import '../css/Groups.css';

const Groups = () => {
  const [inGroup, setInGroup] = useState(false);
  const [groupData, setGroupData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the group data for the user
    const fetchGroupData = async () => {
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('userId');

        // Fetch user data
        const userResponse = await fetch(`http://localhost:5001/user?id=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const userData = await userResponse.json();
        console.log('User data:', userData);

        if (userData.groupid) {
          // Fetch group data
          const groupResponse = await fetch(`http://localhost:5001/group?groupid=${userData.groupid}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
          const groupData = await groupResponse.json();
          console.log('Group data:', groupData);
          setInGroup(true);
          setGroupData({
            groupid: groupData.groupid,
            groupname: groupData.groupname,
            ownerid: groupData.ownerid,
            project: groupData.project,
            group_members: groupData.group_members.map(member => ({
              userid: member[0],
              firstname: member[1],
              lastname: member[2],
            })),
          });
        }
      } catch (error) {
        console.error('Error fetching group data:', error);
      }
    };
    fetchGroupData();
  }, []);

  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="groups-container">
      <header className="groups-header">
        <h1>Manage Group <button onClick={handleBack} className="back-button">Back to Dashboard</button></h1>
      </header>
      <div className='groups-content'>
        {inGroup ? (
          <GroupIn groupData={groupData} />
        ) : (
          <GroupNotIn />
        )}
      </div>
    </div>
  );
};

export default Groups;
