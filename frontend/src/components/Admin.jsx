import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Admin.css';

const ManageSkills = () => {
  const [skillName, setSkillName] = useState('');
  const [skills, setSkills] = useState([]);
  const navigate = useNavigate();

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
      console.log(data);
      if (response.ok) {
        // Convert the object of skills to an array
        const skillsArray = Object.values(data);
        setSkills(skillsArray);
      } else {
        throw new Error('Failed to load skills');
      }
    } catch (error) {
      console.error('Error fetching skills:', error);
      alert('Error fetching skills');
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleCreateSkill = async () => {
    try {
      const formData = new FormData();
      formData.append('skillname', skillName);
      formData.append('userid', localStorage.getItem('userId'));

      const response = await fetch('http://localhost:5001/skill/create', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: formData,
      });

      const text = await response.text();
      if (!response.ok) {
        console.log('Server response:', text);
        throw new Error(text);
      }

      alert('Skill created successfully!');
      setSkillName(''); // Reset the skill name input
      fetchSkills(); // Fetch skills again to update the list
    } catch (error) {
      console.error('Error creating skill:', error);
      alert(error.message);
    }
  };

  const handleBack = () => {
    navigate('/dashboard'); 
  };

  return (
    <div className='manage-skills-container'>
      <header className='manage-skills-header'>
        <h1>Admin Page</h1>
        <button onClick={handleBack} className="back-button">Back to Dashboard</button>
      </header>
      <div className='content'>
        <h2>Manage Skills</h2>
        <p>Enter Skill Name:</p>
        <input
          className='skill-name-input'
          type="text"
          value={skillName}
          onChange={(e) => setSkillName(e.target.value)}
          placeholder="Skill Name"
        />
        <button onClick={handleCreateSkill} className='create-skill-button'>Create Skill</button>

        <h2>Skills List</h2>
        <ul>
          {skills.length > 0 ? (
            skills.map((skill) => (
              <li key={skill.skillid}>{skill.skillname}</li>
            ))
          ) : (
            <li>No skills found</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default ManageSkills;
