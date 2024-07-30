import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Profile.css';
import Modal from './Modal';
import { BackButton, LogoutButton } from './utils';

const Profile = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [hasData, setHasData] = useState(false);
  const [user, setUser] = useState({});
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [isUserDetailSectionCollapsed, setIsUserDetailSectionCollapsed] = useState(true);
  const [skills, setSkills] = useState([]);
  const [studentSkills, setStudentSkills] = useState([]);
  const [isSkillsSectionCollapsed, setIsSkillsSectionCollapsed] = useState(true);

  useEffect(() => {
    // User role from localStorage
    const userRole = localStorage.getItem('role');
    if (userRole) {
      setRole(userRole);
    } else {
      // If no role is found, redirect to the home page or login page
      navigate('/');
    }
    fetchUserData();
    fetchStudentSkills();
    fetchSkills();
  }, [navigate]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');

      // Fetch user data
      const response = await fetch(`http://localhost:5001/user?id=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      const Userdata = await response.json();
      setHasData(true)
      console.log('User data:', Userdata);
      setUser(Userdata);
      setFirstName(Userdata.first_name);
      setLastName(Userdata.last_name);
      setEmail(Userdata.email);
    //   {"userid" : user.userid, "email" : user.email, "first_name" : user.first_name, "last_name" : user.last_name, "role" : user.role, "groupid" : user.groupid}
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
    return;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const userId = localStorage.getItem('userId');
      const token = localStorage.getItem('token');

      const formdata = new FormData();
      formdata.append('user_id', userId);
      formdata.append('firstName', firstName);
      formdata.append('lastName', lastName,);

      const response = await fetch(`http://localhost:5001/updateUserName`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formdata
      });
      const output = await response.json();
      console.log(output)
    }
    
    catch (error) {
      console.error('Error updating user data:', error);
    }
    // Add your form submission logic here
  };
  
  // const HandleLogout = () => {
  //   const navigate = useNavigate();
  //   localStorage.clear();
  //   navigate('/');
  // };

  const toggleUserDetailSection = () => {
    setIsUserDetailSectionCollapsed(!isUserDetailSectionCollapsed);
  };

  const toggleSkillsSection = () => {
    setIsSkillsSectionCollapsed(!isSkillsSectionCollapsed);
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

  const fetchStudentSkills = async () => {
    try {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('userId');
      const studentId = parseInt(localStorage.getItem('role'), 10);
  
      if (isNaN(studentId) || studentId > 0) {
        throw new Error("Invalid student ID");
      }
  
      const response = await fetch(`http://localhost:5001/skills/view/student?userid=${userId}&studentid=${userId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        const text = await response.text();
        console.log('Server response:', text);
        throw new Error(text);
      }
  
      const data = await response.json();
      console.log(data);
      const studentSkillsArray = Object.entries(data).map(([key, value]) => ({ skillid: parseInt(key), skillname: value }));
      setStudentSkills(studentSkillsArray);
    } catch (error) {
      console.error('Error fetching student skills:', error);
      alert(`Error fetching student skills: ${error.message}`);
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

      const text = await response.text();
      if (!response.ok) {
        console.log('Server response:', text);
        throw new Error(text);
      }

      alert('Skill added successfully!');
      fetchStudentSkills(); // Refresh the list of student skills
    } catch (error) {
      console.error('Error adding skill:', error);
      alert(`Error adding skill: ${error.message}`);
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

      const text = await response.text();
      if (!response.ok) {
        throw new Error(text);
      }

      alert('Skill removed successfully!');
      fetchStudentSkills();
    } catch (error) {
      console.error('Error removing skill:', error);
      alert(`Error removing skill: ${error.message}`);
    }
  };
  
  // const handleBack = () => {
  //   navigate('/dashboard');
  // };

  const handleReset = async (e) => {
    navigate('/reset');
  };
  
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        {/* <h1>Profile <button onClick={handleBack} className="back-button">Back to Dashboard</button></h1> */}
        <BackButton />
        <h1>Profile</h1>
        <LogoutButton />
      </header>
      <div className="dashboard-profile-content">
        <div className="dashboard-profile-section">
          <h2>User Detail</h2>
          <div className='dashboard-profile-row'>
            <p><strong>Firstname:</strong> {firstName}</p>
            <p><strong>LastName:</strong> {lastName}</p>
            <p><strong>Email:</strong> <p>{email}</p></p>
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
              <button onClick={(e) => handleSubmit(e)}> update </button>
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
        </div>
        <div className="dashboard-section">
          <button onClick={(e) => handleReset(e)}> Reset Password </button>
        </div>
      </div>
    </div>
  );
};

export default Profile;