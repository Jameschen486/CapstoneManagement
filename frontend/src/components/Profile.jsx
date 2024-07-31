import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Profile.css';

const Profile = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [user, setUser] = useState({});
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [skills, setSkills] = useState([]);
  const [studentSkills, setStudentSkills] = useState([]);
  const [projects, setProjects] = useState([]);
  const [preferences, setPreferences] = useState([]);
  const [isUserDetailSectionCollapsed, setIsUserDetailSectionCollapsed] = useState(true);
  const [isSkillsSectionCollapsed, setIsSkillsSectionCollapsed] = useState(true);
  const [isPreferenceSectionCollapsed, setIsPreferenceSectionCollapsed] = useState(true);

  useEffect(() => {
    const userRole = localStorage.getItem('role');
    if (userRole) {
      setRole(userRole);
    } else {
      navigate('/');
    }
    fetchUserData();
    fetchStudentSkills();
    fetchSkills();
    fetchProjects();
    fetchPreferences();
  }, [navigate]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/user?id=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const data = await response.json();
      setUser(data);
      setFirstName(data.first_name);
      setLastName(data.last_name);
      setEmail(data.email);
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const fetchSkills = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/skills/view?userid=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      setSkills(Object.values(data));
    } catch (error) {
      console.error('Error fetching skills:', error);
      alert('Error fetching skills');
    }
  };

  const fetchStudentSkills = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');
  
      const response = await fetch(`http://localhost:5001/skills/view/student?userid=${userId}&studentid=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      const data = await response.json();
      setStudentSkills(Object.entries(data).map(([key, value]) => ({ skillid: parseInt(key), skillname: value })));
    } catch (error) {
      console.error('Error fetching student skills:', error);
      alert('Error fetching student skills');
    }
  };

  const fetchProjects = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/projects/view?userid=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      setProjects(Object.keys(data).map(key => ({ projectid: key, ...data[key] })));
    } catch (error) {
      console.error('Error fetching projects:', error);
      alert('Error fetching projects');
    }
  };

  const fetchPreferences = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const response = await fetch(`http://localhost:5001/preference/view?user_id=${userId}&student_id=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }

      const data = await response.json();
      console.log('Preferences data:', data);
      const preferencesArray = data.map(({ project_id, rank }) => ({ project_id, rank }));
      setPreferences(preferencesArray);
    } catch (error) {
      console.error('Error fetching preferences:', error);
      alert(`Error fetching preferences: ${error.message}`);
    }
  };

  const handleAddSkill = async (skillId) => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const formData = new FormData();
      formData.append('userid', userId);
      formData.append('studentid', userId);
      formData.append('skillid', skillId);

      const response = await fetch('http://localhost:5001/skill/add/student', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Skill added successfully!');
        fetchStudentSkills();
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
      formData.append('studentid', userId);
      formData.append('skillid', skillId);

      const response = await fetch('http://localhost:5001/skill/remove/student', {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Skill removed successfully!');
        fetchStudentSkills();
      } else {
        const text = await response.text();
        throw new Error(text);
      }
    } catch (error) {
      console.error('Error removing skill:', error);
      alert('Error removing skill');
    }
  };

  const handleAddPreference = async (projectId, rank) => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const formData = new FormData();
      formData.append('user_id', userId);
      formData.append('project_ids', projectId);
      formData.append('ranks', rank);

      const response = await fetch('http://localhost:5001/preference/add', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Preference added successfully!');
        fetchPreferences();
      } else {
        const text = await response.text();
        throw new Error(text);
      }
    } catch (error) {
      console.error('Error adding preference:', error);
      alert('Error adding preference');
    }
  };

  const handleEditPreference = async (projectId, rank) => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      const formData = new FormData();
      formData.append('user_id', userId);
      formData.append('project_ids', projectId);
      formData.append('ranks', rank);

      const response = await fetch('http://localhost:5001/preference/edit', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        alert('Preference updated successfully!');
        fetchPreferences();
      } else {
        const text = await response.text();
        throw new Error(text);
      }
    } catch (error) {
      console.error('Error updating preference:', error);
      alert('Error updating preference');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const userId = localStorage.getItem('userId');
      const token = localStorage.getItem('token');

      const formdata = new FormData();
      formdata.append('user_id', userId);
      formdata.append('firstName', firstName);
      formdata.append('lastName', lastName);

      const response = await fetch(`http://localhost:5001/updateUserName`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formdata
      });
      const output = await response.json();
      console.log(output);
    } catch (error) {
      console.error('Error updating user data:', error);
    }
  };

  const toggleUserDetailSection = () => {
    setIsUserDetailSectionCollapsed(!isUserDetailSectionCollapsed);
  };

  const toggleSkillsSection = () => {
    setIsSkillsSectionCollapsed(!isSkillsSectionCollapsed);
  };

  const togglePreferenceSection = () => {
    setIsPreferenceSectionCollapsed(!isPreferenceSectionCollapsed);
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Profile</h1>
        <button onClick={handleBack} className="back-button">Back</button>
      </header>
      <div className="dashboard-profile-content">
        <div className="dashboard-profile-section">
          <h2>User Detail</h2>
          <div className='dashboard-profile-row'>
            <p><strong>Firstname:</strong> {firstName}</p>
            <p><strong>LastName:</strong> {lastName}</p>
            <p><strong>Email:</strong> {email}</p>
          </div>
          <button onClick={toggleUserDetailSection} className="toggle-button">
            {isUserDetailSectionCollapsed ? 'Update User Detail' : 'Close'}
          </button>
          {!isUserDetailSectionCollapsed && (
            <form onSubmit={handleSubmit}>
              <p>Firstname:
                <input type="text" name="First" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
              </p>
              <p>LastName:
                <input type="text" name="Last" value={lastName} onChange={(e) => setLastName(e.target.value)} />
              </p>
              <p>Email: {email}</p>
              <button type="submit">Save Changes</button>
            </form>
          )}
          <h2 className='skills-header'>User Skills</h2>
          <div className='user-skills-section'>
            <h3 className='skills-list'>Skills List</h3>
            <ul>
              <p>Click on the skill to delete it from your list</p>
              {studentSkills.length > 0 ? (
                studentSkills.map((skill) => (
                  <li key={skill.skillid} onClick={() => handleRemoveSkill(skill.skillid)}>
                    {skill.skillname}
                  </li>
                ))
              ) : (
                <li>No skills found</li>
              )}
            </ul>
            <button onClick={toggleSkillsSection} className="toggle-button">
              {isSkillsSectionCollapsed ? 'Add Skill' : 'Close'}
            </button>
            {!isSkillsSectionCollapsed && (
              <div className='skills-content'>
                <p>Click on a skill to add it to your list:</p>
                <ul>
                  {skills.length > 0 ? (
                    skills.map((skill) => (
                      <li key={skill.skillid} onClick={() => handleAddSkill(skill.skillid)}>
                        {skill.skillname}
                      </li>
                    ))
                  ) : (
                    <li>No skills found</li>
                  )}
                </ul>
              </div>
            )}
          </div>
          <h2 className='preference-header'>User Preferences</h2>
          <div className='user-preference-section'>
            <h3>Current Preferences</h3>
            <ul>
              {preferences.length > 0 ? (
                preferences.map((pref) => (
                  <li key={pref.project_id}>
                    {projects.find(project => project.projectid === pref.project_id)?.title || 'Unknown Project'} - Rank: {pref.rank}
                  </li>
                ))
              ) : (
                <li>No preferences found</li>
              )}
            </ul>
            <div className='preferences-content'>
              <button onClick={togglePreferenceSection} className="toggle-button">
                {isPreferenceSectionCollapsed ? 'Edit Preferences' : 'Close'}
              </button>
              {!isPreferenceSectionCollapsed && (
                <div>
                  <h3>Add/Edit Preferences</h3>
                  <ul>
                    {projects.map((project) => (
                      <li key={project.projectid}>
                        <span>{project.title}</span>
                        <select
                          onChange={(e) => handleAddPreference(project.projectid, e.target.value)}
                          defaultValue={preferences.find(pref => pref.project_id === project.projectid)?.rank || ''}
                        >
                          <option value="" disabled>Select Rank</option>
                          <option value="1">1</option>
                          <option value="2">2</option>
                          <option value="3">3</option>
                        </select>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
