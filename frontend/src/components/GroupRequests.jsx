import React, { useState, useEffect } from 'react';

const GroupRequests = () => {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    // Fetch join requests
    const fetchRequests = async () => {
      try {
        const response = await fetch('/api/group/requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await response.json();
        setRequests(data.requests);
      } catch (error) {
        console.error('Error fetching requests:', error);
      }
    };
    fetchRequests();
  }, []);

  const handleAccept = async (userId) => {
    // Handle accept request
  };

  const handleDeny = async (userId) => {
    // Handle deny request
  };

  return (
    <div className="group-requests">
      <h3>Requests</h3>
      {requests.map((request) => (
        <div key={request.id} className="request-item">
          <span>{request.firstName} {request.lastName}</span>
          <button onClick={() => handleAccept(request.id)}>Accept</button>
          <button onClick={() => handleDeny(request.id)}>Deny</button>
        </div>
      ))}
    </div>
  );
};

export default GroupRequests;
