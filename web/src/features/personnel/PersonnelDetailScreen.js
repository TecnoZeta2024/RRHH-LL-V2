import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Assuming react-router-dom is used
import { getPersonnelDetail, deletePersonnel } from './personnelApi';

function PersonnelDetailScreen() {
  const { id } = useParams(); // Get ID from URL
  const [personnel, setPersonnel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPersonnel = async () => {
      try {
        const data = await getPersonnelDetail(id);
        setPersonnel(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPersonnel();
  }, [id]); // Re-run effect if ID changes

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this personnel?')) {
      try {
        await deletePersonnel(id);
        console.log('Personnel deleted. Navigate back to list.');
        // TODO: Navigate back to personnel list after deletion
      } catch (err) {
        console.error('Error deleting personnel:', err);
        // TODO: Display error message to user
      }
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!personnel) {
    return <div>Personnel not found.</div>;
  }

  return (
    <div>
      <h2>Personnel Detail</h2>
      <p><strong>Name:</strong> {personnel.name}</p>
      <p><strong>Position:</strong> {personnel.position}</p>
      {/* Display other personnel details as needed */}
      <button onClick={() => console.log('Navigate back to list')}>
        Back to List
      </button>
      <button onClick={() => console.log(`Navigate to Edit for ${personnel.id}`)}>
        Edit
      </button>
      <button onClick={handleDelete}>
        Delete
      </button>
    </div>
  );
}

export default PersonnelDetailScreen;
