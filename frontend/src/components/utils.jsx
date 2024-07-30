import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';
import Modal from './Modal';

export function handleLogout(navigate) {
  localStorage.clear(); 
  navigate('/');
}

export function handleBack(navigate) {
  navigate(-1);
}

export const LogoutButton = () => {
  const navigate = useNavigate();
  return (
    <button onClick={() => handleLogout(navigate)} className="logout-button"> Logout </button>
  ) 
};

export const BackButton = () => {
  const navigate = useNavigate();
  return (
    <button onClick={() => handleBack(navigate)} className="back-button"> Back </button>
  )
};
