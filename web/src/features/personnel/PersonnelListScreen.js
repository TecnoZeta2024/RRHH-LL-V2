import React, { useEffect, useState } from 'react';
import { getPersonnel } from './personnelApi';

function PersonnelListScreen() {
  const [personnel, setPersonnel] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPersonnel = async () => {
      try {
        const data = await getPersonnel();
        setPersonnel(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchPersonnel();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div>
      <h2>Personnel List</h2>
      <button onClick={() => console.log('Navigate to Add Personnel Form')}>
        Add Personnel
      </button>
      <ul>
        {personnel.map((person) => (
          <li key={person.id}>
            {person.name} - {person.position}
            <button onClick={() => console.log(`Navigate to Detail for ${person.id}`)}>
              View Detail
            </button>
            <button onClick={() => console.log(`Navigate to Edit for ${person.id}`)}>
              Edit
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PersonnelListScreen;
