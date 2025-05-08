import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // Assuming react-router-dom is used
import { getPersonnelDetail, createPersonnel, updatePersonnel } from './personnelApi';

function PersonnelFormScreen() {
  const { id } = useParams(); // Get ID from URL for editing
  const [formData, setFormData] = useState({ name: '', position: '' });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (id) {
      const fetchPersonnel = async () => {
        try {
          const data = await getPersonnelDetail(id);
          if (data) {
            setFormData({ name: data.name, position: data.position });
          } else {
            setError(new Error('Personnel not found.'));
          }
        } catch (err) {
          setError(err);
        } finally {
          setLoading(false);
        }
      };
      fetchPersonnel();
    } else {
      setLoading(false); // No loading needed for creation
    }
  }, [id]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    // TODO: Add form validation

    try {
      if (id) {
        await updatePersonnel(id, formData);
        console.log('Personnel updated successfully. Navigate back.');
        // TODO: Navigate back to detail or list screen
      } else {
        await createPersonnel(formData);
        console.log('Personnel created successfully. Navigate back.');
        // TODO: Navigate back to list screen
      }
    } catch (err) {
      setError(err);
      console.error('Error submitting form:', err);
      // TODO: Display error message to user
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div>
      <h2>{id ? 'Edit Personnel' : 'Add Personnel'}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <label htmlFor="position">Position:</label>
          <input
            type="text"
            id="position"
            name="position"
            value={formData.position}
            onChange={handleInputChange}
            required
          />
        </div>
        {/* Add other form fields here */}
        <button type="submit" disabled={submitting}>
          {submitting ? 'Saving...' : 'Save'}
        </button>
        <button type="button" onClick={() => console.log('Navigate back/cancel')}>
          Cancel
        </button>
      </form>
    </div>
  );
}

export default PersonnelFormScreen;
