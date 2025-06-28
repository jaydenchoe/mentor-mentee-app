import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Profile({ user }) {
  const [profile, setProfile] = useState({
    name: '',
    bio: '',
    skills: []
  });
  const [newSkill, setNewSkill] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setProfile({
          name: response.data.profile.name,
          bio: response.data.profile.bio || '',
          skills: response.data.profile.skills || []
        });
      } catch (error) {
        console.error('Failed to fetch profile:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value
    });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file
      if (!['image/jpeg', 'image/jpg', 'image/png'].includes(file.type)) {
        setMessage('Please select a JPG or PNG image');
        return;
      }
      if (file.size > 1024 * 1024) { // 1MB
        setMessage('Image size must be less than 1MB');
        return;
      }
      setImageFile(file);
      setMessage('');
    }
  };

  const addSkill = () => {
    if (newSkill.trim() && !profile.skills.includes(newSkill.trim())) {
      setProfile({
        ...profile,
        skills: [...profile.skills, newSkill.trim()]
      });
      setNewSkill('');
    }
  };

  const removeSkill = (skillToRemove) => {
    setProfile({
      ...profile,
      skills: profile.skills.filter(skill => skill !== skillToRemove)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage('');

    try {
      const token = localStorage.getItem('token');
      const updateData = {
        name: profile.name,
        bio: profile.bio
      };

      if (user.role === 'mentor') {
        updateData.skills = profile.skills;
      }

      // Convert image to base64 if provided
      if (imageFile) {
        const reader = new FileReader();
        reader.onload = async () => {
          const base64 = reader.result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
          updateData.image = base64;
          
          await axios.put('/api/profile', updateData, {
            headers: { Authorization: `Bearer ${token}` }
          });
          
          setMessage('Profile updated successfully!');
          setImageFile(null);
        };
        reader.readAsDataURL(imageFile);
      } else {
        await axios.put('/api/profile', updateData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setMessage('Profile updated successfully!');
      }
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h1>Edit Profile</h1>
      
      {message && (
        <div className={message.includes('success') ? 'success-message' : 'error-message'}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={profile.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="bio">Bio</label>
          <textarea
            id="bio"
            name="bio"
            value={profile.bio}
            onChange={handleChange}
            placeholder="Tell others about yourself..."
          />
        </div>

        <div className="form-group">
          <label htmlFor="image">Profile Image (JPG/PNG, max 1MB, 500x500 to 1000x1000)</label>
          <input
            type="file"
            id="image"
            accept="image/jpeg,image/jpg,image/png"
            onChange={handleImageChange}
          />
        </div>

        {user.role === 'mentor' && (
          <div className="form-group">
            <label>Skills</label>
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <input
                type="text"
                value={newSkill}
                onChange={(e) => setNewSkill(e.target.value)}
                placeholder="Add a skill"
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
              />
              <button type="button" onClick={addSkill} className="btn">Add</button>
            </div>
            <div className="skills">
              {profile.skills.map((skill, index) => (
                <span key={index} className="skill-tag">
                  {skill}
                  <button
                    type="button"
                    onClick={() => removeSkill(skill)}
                    style={{ 
                      marginLeft: '0.5rem', 
                      background: 'none', 
                      border: 'none', 
                      color: '#e74c3c',
                      cursor: 'pointer'
                    }}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>
        )}

        <button type="submit" className="btn" disabled={saving}>
          {saving ? 'Saving...' : 'Update Profile'}
        </button>
      </form>
    </div>
  );
}

export default Profile;
