import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MentorList() {
  const [mentors, setMentors] = useState([]);
  const [filteredMentors, setFilteredMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    skill: '',
    orderBy: ''
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchMentors();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [mentors, filters]);

  const fetchMentors = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/mentors', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMentors(response.data);
    } catch (error) {
      console.error('Failed to fetch mentors:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...mentors];

    // Filter by skill
    if (filters.skill) {
      filtered = filtered.filter(mentor =>
        mentor.skills.some(skill =>
          skill.toLowerCase().includes(filters.skill.toLowerCase())
        )
      );
    }

    // Sort
    if (filters.orderBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (filters.orderBy === 'skill') {
      filtered.sort((a, b) => {
        const aSkills = a.skills.join(', ');
        const bSkills = b.skills.join(', ');
        return aSkills.localeCompare(bSkills);
      });
    }

    setFilteredMentors(filtered);
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const sendMatchRequest = async (mentorId) => {
    const message = prompt('Enter a message for the mentor (optional):');
    if (message === null) return; // User cancelled

    try {
      const token = localStorage.getItem('token');
      await axios.post('/api/match-requests', {
        mentorId,
        message
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage('Match request sent successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to send match request');
    }
  };

  if (loading) {
    return <div className="loading">Loading mentors...</div>;
  }

  return (
    <div className="container">
      <h1>Find Mentors</h1>

      {message && (
        <div className={message.includes('success') ? 'success-message' : 'error-message'}>
          {message}
        </div>
      )}

      <div className="filter-container">
        <input
          type="text"
          name="skill"
          placeholder="Filter by skill"
          value={filters.skill}
          onChange={handleFilterChange}
        />
        <select name="orderBy" value={filters.orderBy} onChange={handleFilterChange}>
          <option value="">Sort by</option>
          <option value="name">Name</option>
          <option value="skill">Skills</option>
        </select>
      </div>

      {filteredMentors.length === 0 ? (
        <p>No mentors found.</p>
      ) : (
        <div className="mentor-grid">
          {filteredMentors.map(mentor => (
            <div key={mentor.id} className="mentor-card">
              <img 
                src={mentor.imageUrl} 
                alt={mentor.name}
                className="mentor-image"
                onError={(e) => {
                  e.target.src = 'https://placehold.co/500x500.jpg?text=MENTOR';
                }}
              />
              <div className="mentor-name">{mentor.name}</div>
              <div className="mentor-bio">{mentor.bio || 'No bio available'}</div>
              <div className="skills">
                {mentor.skills.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                ))}
              </div>
              <button 
                className="btn" 
                onClick={() => sendMatchRequest(mentor.id)}
              >
                Send Match Request
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MentorList;
