import React, { useEffect, useState } from 'react';
import '../css/ProjectDetailsModal.css';

const ProjectDetailsModal = ({ projectId, onClose }) => {
  const [projectDetails, setProjectDetails] = useState(null);
  const [ownerDetails, setOwnerDetails] = useState(null);
  const [projectSkills, setProjectSkills] = useState([]);
  const [allSkills, setAllSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditMode, setIsEditMode] = useState(false);
  const [updatedProjectDetails, setUpdatedProjectDetails] = useState({});

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
      setUpdatedProjectDetails(projectData);

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

      fetchProjectSkills();
      fetchAllSkills();
    } catch (error) {
      setError('Failed to load details');
      console.error('Fetch details error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (projectId) {
      fetchProjectDetails();
    }
  }, [projectId]);

  const fetchProjectSkills = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/skills/view/project?userid=${userId}&projectid=${projectId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch project skills');
      }

      const data = await response.json();
      setProjectSkills(Object.entries(data).map(([key, value]) => ({ skillid: parseInt(key), skillname: value })));
    } catch (error) {
      console.error('Error fetching project skills:', error);
      alert('Error fetching project skills');
    }
  };

  const fetchAllSkills = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/skills/view?userid=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch all skills');
      }

      const data = await response.json();
      setAllSkills(Object.values(data));
    } catch (error) {
      console.error('Error fetching all skills:', error);
      alert('Error fetching all skills');
    }
  };

  const handleAddSkill = async (skillId) => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const formData = new FormData();
      formData.append('userid', userId);
      formData.append('projectid', projectId);
      formData.append('skillid', skillId);

      const response = await fetch('http://localhost:5001/skill/add/project', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Skill added successfully!');
        fetchProjectSkills();
      } else {
        const text = await response.text();
        throw new Error(text);
      }
    } catch (error) {
      console.error('Error adding skill:', error);
      alert('Error adding skill');
    }
  };

  const handleRemoveSkill = async (skillId) => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const formData = new FormData();
      formData.append('userid', userId);
      formData.append('projectid', projectId);
      formData.append('skillid', skillId);

      const response = await fetch('http://localhost:5001/skill/remove/project', {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Skill removed successfully!');
        fetchProjectSkills();
      } else {
        const text = await response.text();
        throw new Error(text);
      }
    } catch (error) {
      console.error('Error removing skill:', error);
      alert('Error removing skill');
    }
  };

  const handleUpdateProject = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const formData = new FormData();
      formData.append('userid', userId);
      formData.append('projectid', projectId);
      Object.keys(updatedProjectDetails).forEach(key => {
        formData.append(key, updatedProjectDetails[key]);
      });

      const response = await fetch('http://localhost:5001/project/update', {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Project updated successfully!');
        setIsEditMode(false);
        fetchProjectDetails();
      } else {
        const text = await response.text();
        throw new Error(text);
      }
    } catch (error) {
      console.error('Error updating project:', error);
      alert('Error updating project');
    }
  };

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
            <p>Name: {ownerDetails ? `${ownerDetails.first_name} ${ownerDetails.last_name}` : 'Loading...'}</p>
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
            <p><strong>Skills:</strong></p>
            <ul>
              {projectSkills.length > 0 ? (
                projectSkills.map(skill => (
                  <li key={skill.skillid} onClick={() => handleRemoveSkill(skill.skillid)}>
                    {skill.skillname}
                  </li>
                ))
              ) : (
                <li>No skills assigned to this project</li>
              )}
            </ul>
            <div className='skills-content'>
              <p>Click on a skill to add it to the project:</p>
              <ul>
                {allSkills.length > 0 ? (
                  allSkills.map((skill) => (
                    <li key={skill.skillid} onClick={() => handleAddSkill(skill.skillid)}>
                      {skill.skillname}
                    </li>
                  ))
                ) : (
                  <li>No skills found</li>
                )}
              </ul>
            </div>
            <button onClick={() => setIsEditMode(true)} className="edit-button">Edit Project</button>
            {isEditMode && (
              <form onSubmit={handleUpdateProject} className="update-form">
                <p>Please Note that project title needs to be changed to update fields</p>
                <label>
                  Title:
                  <input
                    type="text"
                    value={updatedProjectDetails.title}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, title: e.target.value })}
                  />
                </label>
                <label>
                  Channel:
                  <input
                    type="text"
                    value={updatedProjectDetails.channel}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, channel: e.target.value })}
                  />
                </label>
                <label>
                  Group Count:
                  <input
                    type="number"
                    value={updatedProjectDetails.groupcount}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, groupcount: e.target.value })}
                  />
                </label>
                <label>
                  Specializations:
                  <input
                    type="text"
                    value={updatedProjectDetails.specializations}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, specializations: e.target.value })}
                  />
                </label>
                <label>
                  Background:
                  <textarea
                    value={updatedProjectDetails.background}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, background: e.target.value })}
                  />
                </label>
                <label>
                  Requirements:
                  <textarea
                    value={updatedProjectDetails.requirements}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, requirements: e.target.value })}
                  />
                </label>
                <label>
                  Required Knowledge:
                  <textarea
                    value={updatedProjectDetails.reqknowledge}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, reqknowledge: e.target.value })}
                  />
                </label>
                <label>
                  Outcomes:
                  <textarea
                    value={updatedProjectDetails.outcomes}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, outcomes: e.target.value })}
                  />
                </label>
                <label>
                  Supervision:
                  <textarea
                    value={updatedProjectDetails.supervision}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, supervision: e.target.value })}
                  />
                </label>
                <label>
                  Clients:
                  <textarea
                    value={updatedProjectDetails.clients}
                    onChange={(e) => setUpdatedProjectDetails({ ...updatedProjectDetails, clients: e.target.value })}
                  />
                </label>
                <button type="submit" className="save-button">Save</button>
                <button onClick={() => setIsEditMode(false)} className="cancel-button">Cancel</button>
              </form>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectDetailsModal;
