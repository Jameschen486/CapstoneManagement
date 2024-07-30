import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Profile.css';
import Modal from './Modal';

const Profile = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [hasData, setHasData] = useState(false);
  const [user, setUser] = useState({});
  const [showNotificationModal, setShowNotificationModal] = useState(false);
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [isUserDetailSectionCollapsed, setIsUserDetailSectionCollapsed] = useState(true);

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
      setUser({
        first: Userdata.first_name,
        last: Userdata.last_name,
        email: Userdata.email,
      });
      setFirstName(Userdata.first_name);
      setLastName(Userdata.last_name);
      setEmail(Userdata.email);
    //   {"userid" : user.userid, "email" : user.email, "first_name" : user.first_name, "last_name" : user.last_name, "role" : user.role, "groupid" : user.groupid}
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
    return;
  };

  // console.log('User data:', userData);
  console.log("outside Async");
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

  const toggleUserDetailSection = () => {
    setIsUserDetailSectionCollapsed(!isUserDetailSectionCollapsed);
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
                {console.log(user.first)}
                <p><strong>Firstname:</strong>
                  {firstName}
                </p>
                
                <p><strong>LastName:</strong>
                  {lastName}
                </p>
                
                <p><strong>Email:</strong>
                <p>{email}</p>
                </p>       
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
          <div className='user-skills-section'>
            <h2>User Skills</h2>
          </div>
        </div>
      </div>
      <Modal show={showNotificationModal} handleClose={() => setShowNotificationModal(false)} title="Notifications">
        <p>No notifications yet.</p>
      </Modal>
      <Modal show={showMessageModal} handleClose={() => setShowMessageModal(false)} title="Messages">
        <p>No messages yet.</p>
      </Modal>
    </div>
  );
};

export default Profile;
