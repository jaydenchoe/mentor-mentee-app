import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MatchRequests({ user }) {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchRequests();
  }, [user.role]);

  const fetchRequests = async () => {
    try {
      const token = localStorage.getItem('token');
      const endpoint = user.role === 'mentor' ? '/api/match-requests/incoming' : '/api/match-requests/outgoing';
      const response = await axios.get(endpoint, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRequests(response.data);
    } catch (error) {
      console.error('Failed to fetch requests:', error);
    } finally {
      setLoading(false);
    }
  };

  const respondToRequest = async (requestId, action) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(`/api/match-requests/${requestId}/respond`, {
        action
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage(`Request ${action}ed successfully!`);
      fetchRequests(); // Refresh the list
    } catch (error) {
      setMessage(error.response?.data?.error || `Failed to ${action} request`);
    }
  };

  const deleteRequest = async (requestId) => {
    if (!window.confirm('Are you sure you want to delete this request?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.delete(`/api/match-requests/${requestId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage('Request deleted successfully!');
      fetchRequests(); // Refresh the list
    } catch (error) {
      setMessage(error.response?.data?.error || 'Failed to delete request');
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'pending': return 'status-badge status-pending';
      case 'accepted': return 'status-badge status-accepted';
      case 'rejected': return 'status-badge status-rejected';
      default: return 'status-badge';
    }
  };

  if (loading) {
    return <div className="loading">Loading requests...</div>;
  }

  return (
    <div className="container">
      <h1>
        {user.role === 'mentor' ? 'Incoming Match Requests' : 'My Match Requests'}
      </h1>

      {message && (
        <div className={message.includes('success') ? 'success-message' : 'error-message'}>
          {message}
        </div>
      )}

      {requests.length === 0 ? (
        <p>No match requests found.</p>
      ) : (
        <div className="request-list">
          {requests.map(request => (
            <div key={request.id} className="request-card">
              <div className="request-header">
                <div>
                  {user.role === 'mentor' ? (
                    <div>
                      <strong>{request.mentee.name}</strong>
                      <p>{request.mentee.bio || 'No bio available'}</p>
                    </div>
                  ) : (
                    <div>
                      <strong>{request.mentor.name}</strong>
                      <p>{request.mentor.bio || 'No bio available'}</p>
                    </div>
                  )}
                </div>
                <span className={getStatusBadgeClass(request.status)}>
                  {request.status.toUpperCase()}
                </span>
              </div>

              {request.message && (
                <div style={{ marginBottom: '1rem' }}>
                  <strong>Message:</strong> {request.message}
                </div>
              )}

              <div style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1rem' }}>
                Sent: {new Date(request.createdAt).toLocaleDateString()}
              </div>

              {user.role === 'mentor' && request.status === 'pending' && (
                <div className="request-actions">
                  <button 
                    className="btn btn-success"
                    onClick={() => respondToRequest(request.id, 'accept')}
                  >
                    Accept
                  </button>
                  <button 
                    className="btn btn-danger"
                    onClick={() => respondToRequest(request.id, 'reject')}
                  >
                    Reject
                  </button>
                </div>
              )}

              {user.role === 'mentee' && request.status === 'pending' && (
                <div className="request-actions">
                  <button 
                    className="btn btn-danger"
                    onClick={() => deleteRequest(request.id)}
                  >
                    Cancel Request
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MatchRequests;
