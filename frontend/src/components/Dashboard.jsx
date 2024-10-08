import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';
import Modal from './Modal';
import {GroupIn} from './GroupIn';
import { NotificationBox } from './utils';

const Dashboard = () => {
  const navigate = useNavigate();
  const [role, setRole] = useState('');
  const [showNotificationModal, setShowNotificationModal] = useState(false);
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [email1, setEmail1] = useState('');
  const [password, setPassword] = useState('');
  const [email2, setEmail2] = useState('');
  const [newRole, setNewRole] = useState('');
  const [message, setMessage] = useState('');
  const [isRoleSectionCollapsed, setIsRoleSectionCollapsed] = useState(true);
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [groupData, setGroupData] = useState(null);

  const roleOptions = {
    'Student': 0,
    'Tutor': 1,
    'Coordinator': 2,
    'Admin': 3,
    'Client': 4
  };

  useEffect(() => {
    const userRole = localStorage.getItem('role');
    if (userRole) {
      setRole(userRole);
    } else {
      navigate('/');
    }
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
          // setInGroup(true);
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
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate('/');
  };

  const handleGroupsClick = () => {
    navigate('/groups');
  };

  const handleProfileClick = () => {
    navigate('/profile');
  };
  const handleAdminClick = () => {
    navigate('/admin');
  };

  const handleProjectsClick = () => {
    navigate('/projects');
  };

  const handleRoleChange = async (e) => {
    e.preventDefault();

    const roleValue = roleOptions[newRole];
    console.log('Selected role:', newRole); // Debugging log
    console.log('Mapped role value:', roleValue); // Debugging log

    if (roleValue === undefined) {
      setMessage('Please select a valid role.');
      return;
    }

    const formData = new FormData();
    formData.append('email1', email1);
    formData.append('password', password);
    formData.append('email2', email2);
    formData.append('role', roleValue);

    try {
      const response = await fetch('http://localhost:5001/updateUserRole', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('User role updated successfully.');
        setFormSubmitted(true); // Hide the form
        setEmail1('');
        setPassword('');
        setEmail2('');
        setNewRole('');
      } else {
        setMessage(data.error || 'Failed to update user role.');
      }
    } catch (error) {
      console.error('Error updating user role:', error);
      setMessage('An error occurred. Please try again later.');
    }
  };

  const toggleRoleSection = () => {
    setIsRoleSectionCollapsed(!isRoleSectionCollapsed);
    setMessage('');
    setFormSubmitted(false); // Show the form again when the section is toggled
  };

  const renderDashboardContent = () => {
    switch (role) {
      case '0':
        return (
          <div className="dashboard-section">
            <div className='dashboard-header-row'>
              <h2>Student Dashboard</h2>
              <div className="dashboard-icons">
                <div className="icon-container">
                  <button onClick={() => setShowNotificationModal(true)} aria-label="Notifications">&#128276;</button>
                  <span className="icon-label">Notifications</span>
                </div>
                <div className="icon-container">
                  <button onClick={() => setShowMessageModal(true)} aria-label="Messages">&#128172;</button>
                  <span className="icon-label">Messages</span>
                </div>
                <div className="icon-container">
                  <button onClick={handleProfileClick} aria-label="Profile">&#128100;</button>
                  <span className="icon-label">Profile</span>
                </div>
                <div className="icon-container">
                  <button onClick={handleGroupsClick} aria-label="Groups">&#128101;</button>
                  <span className="icon-label">Groups</span>
                </div>
              </div>
            </div>
            <p>Here you can manage your projects, view messages, and notifications.</p>
            <h2>Your Group:</h2>
            {groupData ? (<><GroupIn groupData={groupData}/></>):(<></>)}
          </div>
        );
      case '1':
        return (
          <div className="dashboard-section">
            <h2>Tutor Dashboard</h2>
            <p>Here you can manage your projects, view messages, student preferences, and notifications.</p>
          </div>
        );
      case '2':
        return (
          <div className="dashboard-section">
            <h2>Coordinator Dashboard</h2>
            <p>Here you can manage your students, view messages, and notifications.</p>
          </div>
        );
      case '3':
        return (
          <div className="dashboard-section">
            <div className='dashboard-header-row'>
              <h2>Admin Dashboard</h2>
              <div className="dashboard-icons">
                <div className="icon-container">
                  <button onClick={() => setShowNotificationModal(true)} aria-label="Notifications">&#128276;</button>
                  <span className="icon-label">Notifications</span>
                </div>
                <div className="icon-container">
                  <button onClick={() => setShowMessageModal(true)} aria-label="Messages">&#128172;</button>
                  <span className="icon-label">Messages</span>
                </div>
                <div className="icon-container">
                  <button aria-label="Profile">&#128100;</button>
                  <span className="icon-label">Profile</span>
                </div>
                <div className="icon-container">
                  <button onClick={handleAdminClick} aria-label="Admin">&#128119;</button>
                  <span className="icon-label">Admin</span>
                </div>
              </div>
            </div>
            <p>Here you can manage your systems, view messages, and notifications.</p>
            <div className="role-change-section">
              <h3>Modify User Role:</h3>
              <button onClick={toggleRoleSection} className="role-change-toggle-button">
                &#9997;
                {isRoleSectionCollapsed ? 'Open Change User Role' : 'Close Change User Role'}
              </button>
              {!isRoleSectionCollapsed && !formSubmitted && (
                <form className="role-change-form" onSubmit={handleRoleChange}>
                  <h3>Change User Role</h3>
                  {message && <p className="message">{message}</p>}
                  <div className="form-group">
                    <label>Admin Email:</label>
                    <input
                      type="email"
                      placeholder="Admin Email"
                      value={email1}
                      onChange={(e) => setEmail1(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Admin Password:</label>
                    <input
                      type="password"
                      placeholder="Admin Password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>User Email:</label>
                    <input
                      type="email"
                      placeholder="User Email"
                      value={email2}
                      onChange={(e) => setEmail2(e.target.value)}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>New Role:</label>
                    <select
                      value={newRole}
                      onChange={(e) => {
                        setNewRole(e.target.value);
                        console.log('Selected role:', e.target.value); // Debugging log
                        console.log('Mapped role value:', roleOptions[e.target.value]); // Debugging log
                      }}
                      required
                    >
                      <option value="" disabled>Select Role</option>
                      {Object.keys(roleOptions).map((roleName) => (
                        <option key={roleName} value={roleName}>
                          {roleName}
                        </option>
                      ))}
                    </select>
                  </div>
                  <button type="submit" className="role-change-button">Change Role</button>
                </form>
              )}
              {formSubmitted && (
                <p className="message">{message}</p>
              )}
            </div>
          </div>
        );
      case '4':
        return (
          <div className="dashboard-section">
            <div className='dashboard-header-row'>
              <h2>Client Dashboard</h2>
              <div className="dashboard-icons">
                <div className="icon-container">
                  <button onClick={() => setShowNotificationModal(true)} aria-label="Notifications">&#128276;</button>
                  <span className="icon-label">Notifications</span>
                </div>
                <div className="icon-container">
                  <button onClick={() => setShowMessageModal(true)} aria-label="Messages">&#128488;</button>
                  <span className="icon-label">Messages</span>
                </div>
                <div className="icon-container">
                  <button aria-label="Profile">&#128100;</button>
                  <span className="icon-label">Profile</span>
                </div>
                <div className="icon-container">
                  <button aria-label="Student Preference">&#128101;</button>
                  <span className="icon-label">Students</span>
                </div>
              </div>
            </div>
            <p>Here you can manage your projects, view messages, student preferences and notifications.</p>
            <div className="icon-container">
                  <button onClick={handleProjectsClick} aria-label="Projects">&#128202; Manage Projects and Skills</button>
                </div>
          </div>
        );
      default:
        return (
          <div className="dashboard-section">
            <h2>Dashboard</h2>
            <p>Here you can manage your projects, view messages, and notifications.</p>
          </div>
        );
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to Your Dashboard</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>
      <div className="dashboard-content">
        {renderDashboardContent()}
      </div>
      
      <Modal show={showNotificationModal} handleClose={() => setShowNotificationModal(false)} title="Notifications">
        <NotificationBox/>
      </Modal>
      <Modal show={showMessageModal} handleClose={() => setShowMessageModal(false)} title="Messages">
        <p>No messages yet.</p>
      </Modal>
    </div>
  );
};
export default Dashboard;
