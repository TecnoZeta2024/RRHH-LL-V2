// This file will contain API call functions for personnel

const API_BASE_URL = 'YOUR_BACKEND_API_URL'; // Replace with your actual backend URL

export const getAllPersonnel = async () => {
  console.log('Simulating GET all personnel API call');
  // In a real application, use fetch or Axios to call the backend API
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        { id: '1', name: 'John Doe', title: 'Field Worker' },
        { id: '2', name: 'Jane Smith', title: 'Supervisor' },
        { id: '3', name: 'Peter Jones', title: 'Field Worker' },
      ]);
    }, 1000);
  });
};

export const getPersonnelById = async (id) => {
  console.log(`Simulating GET personnel by ID API call for ID: ${id}`);
  // In a real application, use fetch or Axios to call the backend API
  return new Promise((resolve) => {
    setTimeout(() => {
      const dummyPersonnelDetails = {
        '1': { name: 'John Doe', title: 'Field Worker', phone: '123-456-7890', email: 'john.doe@example.com' },
        '2': { name: 'Jane Smith', title: 'Supervisor', phone: '987-654-3210', email: 'jane.smith@example.com' },
        '3': { name: 'Peter Jones', title: 'Field Worker', phone: '555-123-4567', email: 'peter.jones@example.com' },
      };
      resolve(dummyPersonnelDetails[id]);
    }, 1000);
  });
};

export const createPersonnel = async (personnelData) => {
  console.log('Simulating POST create personnel API call with data:', personnelData);
  // In a real application, use fetch or Axios to call the backend API
  return new Promise((resolve) => {
    setTimeout(() => {
      // Simulate a successful creation
      resolve({ id: Date.now().toString(), ...personnelData });
    }, 1000);
  });
};

export const updatePersonnel = async (id, personnelData) => {
  console.log(`Simulating PUT update personnel API call for ID: ${id} with data:`, personnelData);
  // In a real application, use fetch or Axios to call the backend API
  return new Promise((resolve) => {
    setTimeout(() => {
      // Simulate a successful update
      resolve({ id, ...personnelData });
    }, 1000);
  });
};

export const deletePersonnel = async (id) => {
  console.log(`Simulating DELETE personnel API call for ID: ${id}`);
  // In a real application, use fetch or Axios to call the backend API
  return new Promise((resolve) => {
    setTimeout(() => {
      // Simulate a successful deletion
      resolve({ success: true });
    }, 1000);
  });
};
