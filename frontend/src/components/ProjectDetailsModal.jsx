import React, { useState, useEffect } from 'react';
import '../css/ProjectDetailsModal.css'

const ProjectDetailsModal = ({ projectId, onClose }) => {
  const [projectDetails, setProjectDetails] = useState(null);
  const [ownerDetails, setOwnerDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProjectDetails = async () => {
      try {
        setLoading(true);
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('userId');

        const response = await fetch(`http://localhost:5001/project/details?userid=${userId}&projectid=${projectId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch project details');
        }

        const projectData = await response.json();
        setProjectDetails(projectData);

        // Fetch owner details
        const ownerResponse = await fetch(`http://localhost:5001/user?id=${projectData.ownerid}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!ownerResponse.ok) {
          throw new Error('Failed to fetch owner details');
        }

        const ownerData = await ownerResponse.json();
        setOwnerDetails(ownerData);
      } catch (error) {
        setError('Failed to load details');
        console.error('Fetch details error:', error);
      } finally {
        setLoading(false);
      }
    };

    if (projectId) {
      fetchProjectDetails();
    }
  }, [projectId]);

  return (
    <div className="modal">
      <div className="modal-content">
        <button onClick={onClose} className="close-button">Close</button>
        {loading && <p>Loading...</p>}
        {error && <p>Error: {error}</p>}
        {projectDetails && (
          <div>
            <h2>Project Title: {projectDetails.title || 'No Title'}</h2>
            <p><strong>Owner Details:</strong></p>
            <p>Name: {ownerDetails ? ownerDetails.first_name : 'Loading...'} {ownerDetails ? ownerDetails.last_name : 'Loading...'}</p>
            <p>Email: {ownerDetails ? ownerDetails.email : 'Loading...'}</p>
            <p><strong>Channel:</strong> {projectDetails.channel}</p>
            <p><strong>Group Count:</strong> {projectDetails.groupcount}</p>
            <p><strong>Specializations:</strong> {projectDetails.specializations || 'None'}</p>
            <p><strong>Background:</strong> {projectDetails.background || 'None'}</p>
            <p><strong>Requirements:</strong> {projectDetails.requirements || 'None'}</p>
            <p><strong>Required Knowledge:</strong> {projectDetails.reqknowledge || 'None'}</p>
            <p><strong>Outcomes:</strong> {projectDetails.outcomes || 'None'}</p>
            <p><strong>Supervision:</strong> {projectDetails.supervision || 'None'}</p>
            <p><strong>Clients:</strong> {projectDetails.clients || 'None'}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectDetailsModal;
