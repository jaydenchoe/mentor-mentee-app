import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Header({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    onLogout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="container">
        <h1>Mentor-Mentee Matching</h1>
        {user && (
          <nav className="nav">
            <Link to="/dashboard">
              <button>Dashboard</button>
            </Link>
            <Link to="/profile">
              <button>Profile</button>
            </Link>
            {user.role === 'mentee' && (
              <Link to="/mentors">
                <button>Find Mentors</button>
              </Link>
            )}
            <Link to="/requests">
              <button>Requests</button>
            </Link>
            <button onClick={handleLogout}>Logout</button>
          </nav>
        )}
      </div>
    </header>
  );
}

export default Header;
