import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard({ user }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setProfile(response.data);
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h1>Welcome, {user.name}!</h1>
      <p>Role: {user.role}</p>
      
      {profile && (
        <div style={{ marginTop: '2rem' }}>
          <h2>Your Profile</h2>
          <div className="mentor-card" style={{ maxWidth: '400px' }}>
            <img 
              src={profile.profile.imageUrl} 
              alt={profile.profile.name}
              className="mentor-image"
              onError={(e) => {
                e.target.src = `https://placehold.co/500x500.jpg?text=${user.role.toUpperCase()}`;
              }}
            />
            <div className="mentor-name">{profile.profile.name}</div>
            <div className="mentor-bio">{profile.profile.bio || 'No bio yet'}</div>
            {user.role === 'mentor' && profile.profile.skills && (
              <div className="skills">
                {profile.profile.skills.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      <div style={{ marginTop: '2rem' }}>
        {user.role === 'mentor' ? (
          <div>
            <h3>As a Mentor, you can:</h3>
            <ul style={{ marginLeft: '2rem', marginTop: '1rem' }}>
              <li>View and respond to match requests from mentees</li>
              <li>Update your profile and skills</li>
              <li>Accept one mentee at a time</li>
            </ul>
          </div>
        ) : (
          <div>
            <h3>As a Mentee, you can:</h3>
            <ul style={{ marginLeft: '2rem', marginTop: '1rem' }}>
              <li>Browse and search for mentors</li>
              <li>Send match requests to mentors</li>
              <li>View your sent requests and their status</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
