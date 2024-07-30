import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Register.css';

const Register = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [mobile, setMobile] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('firstName', firstName);
    formData.append('lastName', lastName);
    formData.append('password', password);
    formData.append('mobile', mobile);

    try {
      const response = await fetch('http://localhost:5001/register', {
        method: 'POST',
        body: formData,
      });

      let data;
      try {
        data = await response.json();
      } catch (err) {
        console.error('Invalid JSON response:', err);
        setMessage('An error occurred. Please try again later.');
        return;
      }

      if (response.status === 200) {
        setMessage("Account created successfully. Please log in.");
        setTimeout(() => {
          navigate('/');
        }, 2000);  // Redirect after 2 seconds
      } else if (response.status === 409 || response.status === 400 || response.status === 500) {
        setMessage(data.error || "Account already exists. Please log in or reset your password.");
        setTimeout(() => {
          navigate('/');
        }, 2000);  // Redirect after 2 seconds
      } else {
        setMessage("An error occurred. Please try again.");
      }
    } catch (error) {
      console.error("There was an error registering the user!", error);
      setMessage("An error occurred. Please try again later.");
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  return (
    <div className="register-container">
      <header className="register-header">
        <h1>Registration page <button onClick={handleBack} className="back-button">Back to Home</button></h1>
      </header>
      <div className="register-content">
        {message && <p className="message">{message}</p>}
        <form className="register-form" onSubmit={handleSubmit}>
          <h2>Create a new account</h2>
          <div className="form-group">
            <label>First Name:</label>
            <input
              type="text"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Last Name:</label>
            <input
              type="text"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Mobile number:</label>
            <input
              type="tel"
              placeholder="Mobile number"
              value={mobile}
              onChange={(e) => setMobile(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Confirm Password:</label>
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className='create-account-button'>Create New Account</button>
        </form>
      </div>
    </div>
  );
};

export default Register;
