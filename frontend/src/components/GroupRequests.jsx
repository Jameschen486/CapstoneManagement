import React, { useEffect, useState } from 'react';

const GroupRequests = () => {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('userId');

        const response = await fetch(`http://localhost:5001/user/join_requests?userid=${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await response.json();
        if (response.ok) {
          // Convert the list of tuples to list of objects
          const formattedData = data.join_requests.map(request => ({
            userid: request[0],
            first_name: request[1],
            last_name: request[2]
          }));
          setRequests(formattedData || []);
        } else {
          console.error(data.message || 'Error fetching join requests');
        }
      } catch (error) {
        console.error('Error fetching join requests:', error);
      }
    };
    fetchRequests();
  }, []);

  const handleRequest = async (applicantId, accept) => {
    try {
      const formData = new FormData();
      formData.append('userid', localStorage.getItem('userId'));
      formData.append('applicantid', applicantId);
      formData.append('groupid', localStorage.getItem('groupId'));
      formData.append('accept', accept);

      const response = await fetch('http://localhost:5001/group/request/handle', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: formData,
      });

      const data = await response.json();
      console.log(data); // Log the response for debugging
      if (response.ok) {
        alert(data.message);
        // Refresh the join requests
        setRequests(requests.filter(req => req.userid !== applicantId));
      } else {
        alert(data.description || 'Failed to handle join request');
      }
    } catch (error) {
      console.error('Error handling join request:', error);
    }
  };

  return (
    <div className="group-requests">
      <h3>Join Requests</h3>
      {requests.length > 0 ? (
        requests.map((request) => (
          <div key={request.userid} className="request-item">
            <span>{request.first_name} {request.last_name}</span>
            <button onClick={() => handleRequest(request.userid, true)}>Accept</button>
            <button onClick={() => handleRequest(request.userid, false)}>Decline</button>
          </div>
        ))
      ) : (
        <p>No join requests</p>
      )}
    </div>
  );
};

export default GroupRequests;
