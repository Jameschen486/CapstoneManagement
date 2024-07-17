import React, { useState, useEffect } from 'react';
import GroupNotIn from './GroupNotIn';
import GroupIn from './GroupIn';
import '../css/Groups.css';

const Groups = () => {
  const [inGroup, setInGroup] = useState(false);
  const [groupData, setGroupData] = useState(null);

  useEffect(() => {
    // Fetch the group data for the user
    const fetchGroupData = async () => {
      try {
        const response = await fetch('/api/group', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        if (data.group) {
          setInGroup(true);
          setGroupData(data.group);
        }
      } catch (error) {
        console.error('Error fetching group data:', error);
      }
    };
    fetchGroupData();
  }, []);

  return (
    <div className="groups-container">
      {inGroup ? (
        <GroupIn groupData={groupData} />
      ) : (
        <GroupNotIn />
      )}
    </div>
  );
};

export default Groups;
