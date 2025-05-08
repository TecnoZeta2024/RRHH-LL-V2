import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PersonnelListScreen from './PersonnelListScreen';
import { getPersonnel } from './personnelApi';
import { useNavigate } from 'react-router-dom'; // Assuming react-router-dom is used

// Mock the personnelApi module
jest.mock('./personnelApi');

// Mock the react-router-dom useNavigate hook
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

describe('PersonnelListScreen', () => {
  let mockNavigate;

  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    // Reset the mock navigate function before each test
    mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);
  });

  test('renders without crashing and shows loading state', () => {
    // Mock getPersonnel to return a promise that resolves later
    getPersonnel.mockImplementation(() => new Promise(() => {}));

    render(<PersonnelListScreen />);

    // Check if loading state is displayed
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders personnel list after fetching', async () => {
    const mockPersonnel = [
      { id: '1', name: 'John Doe', position: 'Engineer' },
      { id: '2', name: 'Jane Smith', position: 'Designer' },
    ];
    getPersonnel.mockResolvedValue(mockPersonnel);

    render(<PersonnelListScreen />);

    // Wait for the personnel list to load
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Check if personnel names and positions are displayed
    expect(screen.getByText('John Doe - Engineer')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith - Designer')).toBeInTheDocument();
  });

  test('navigates to correct screens on button clicks', async () => {
    const mockPersonnel = [
      { id: '1', name: 'John Doe', position: 'Engineer' },
      { id: '2', name: 'Jane Smith', position: 'Designer' },
    ];
    getPersonnel.mockResolvedValue(mockPersonnel);

    render(<PersonnelListScreen />);

    // Wait for the personnel list to load
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Click "Add Personnel" button
    fireEvent.click(screen.getByText('Add Personnel'));
    expect(mockNavigate).toHaveBeenCalledWith('/personnel/add'); // Assuming '/personnel/add' is the route for adding personnel

    // Click "View Detail" button for the first personnel
    fireEvent.click(screen.getByText('View Detail'));
    expect(mockNavigate).toHaveBeenCalledWith('/personnel/1'); // Assuming '/personnel/:id' is the route for personnel detail

    // Click "Edit" button for the first personnel
    fireEvent.click(screen.getByText('Edit'));
    expect(mockNavigate).toHaveBeenCalledWith('/personnel/edit/1'); // Assuming '/personnel/edit/:id' is the route for editing personnel
  });

  test('displays error message if fetching fails', async () => {
    const errorMessage = 'Failed to fetch personnel';
    getPersonnel.mockRejectedValue(new Error(errorMessage));

    render(<PersonnelListScreen />);

    // Wait for the loading state to disappear and error message to appear
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeTheDocument());

    // Check if the error message is displayed
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });
});

describe('PersonnelDetailScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders without crashing and shows loading state', () => {
    // Mock useParams to return an ID
    useParams.mockReturnValue({ id: '1' });
    // Mock getPersonnelDetail to return a promise that resolves later
    getPersonnelDetail.mockImplementation(() => new Promise(() => {}));

    render(<PersonnelDetailScreen />);

    // Check if loading state is displayed
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders personnel details after fetching', async () => {
    const mockPersonnel = { id: '1', name: 'John Doe', position: 'Engineer', department: 'Engineering' };
    useParams.mockReturnValue({ id: '1' });
    getPersonnelDetail.mockResolvedValue(mockPersonnel);

    render(<PersonnelDetailScreen />);

    // Wait for the loading state to disappear
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Check if personnel details are displayed
    expect(screen.getByText('Personnel Detail')).toBeInTheDocument();
    expect(screen.getByText(`Name: ${mockPersonnel.name}`)).toBeInTheDocument();
    expect(screen.getByText(`Position: ${mockPersonnel.position}`)).toBeInTheDocument();
    // Add assertions for other details as needed
  });

  test('displays error message if fetching fails', async () => {
    const errorMessage = 'Failed to fetch personnel detail';
    useParams.mockReturnValue({ id: '1' });
    getPersonnelDetail.mockRejectedValue(new Error(errorMessage));

    render(<PersonnelDetailScreen />);

    // Wait for the loading state to disappear
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Check if the error message is displayed
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });

  test('displays "Personnel not found" if personnel does not exist', async () => {
    useParams.mockReturnValue({ id: 'non-existent-id' });
    getPersonnelDetail.mockResolvedValue(null);

    render(<PersonnelDetailScreen />);

    // Wait for the loading state to disappear
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeTheDocument());

    // Check if "Personnel not found" message is displayed
    expect(screen.getByText('Personnel not found.')).toBeInTheDocument();
  });

  test('navigates to correct screens and handles deletion', async () => {
    const mockPersonnel = { id: '1', name: 'John Doe', position: 'Engineer', department: 'Engineering' };
    useParams.mockReturnValue({ id: '1' });
    getPersonnelDetail.mockResolvedValue(mockPersonnel);
    deletePersonnel.mockResolvedValue({}); // Mock successful deletion

    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    // Mock window.confirm
    const confirmSpy = jest.spyOn(window, 'confirm');
    confirmSpy.mockReturnValue(true); // Simulate user clicking OK

    render(<PersonnelDetailScreen />);

    // Wait for the personnel details to load
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Click "Back to List" button
    fireEvent.click(screen.getByText('Back to List'));
    expect(mockNavigate).toHaveBeenCalledWith('/personnel'); // Assuming '/personnel' is the route for the personnel list

    // Click "Edit" button
    fireEvent.click(screen.getByText('Edit'));
    expect(mockNavigate).toHaveBeenCalledWith('/personnel/edit/1'); // Assuming '/personnel/edit/:id' is the route for editing personnel

    // Click "Delete" button
    fireEvent.click(screen.getByText('Delete'));

    // Check if window.confirm was called
    expect(confirmSpy).toHaveBeenCalledWith('Are you sure you want to delete this personnel?');

    // Check if deletePersonnel API was called
    expect(deletePersonnel).toHaveBeenCalledWith('1');

    // Wait for navigation after deletion
    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/personnel'));

    // Test delete cancellation
    confirmSpy.mockReturnValue(false); // Simulate user clicking Cancel
    fireEvent.click(screen.getByText('Delete'));
    expect(deletePersonnel).not.toHaveBeenCalledTimes(2); // Ensure deletePersonnel was not called again
  });

  test('handles delete error', async () => {
    const mockPersonnel = { id: '1', name: 'John Doe', position: 'Engineer', department: 'Engineering' };
    const errorMessage = 'Failed to delete personnel';
    useParams.mockReturnValue({ id: '1' });
    getPersonnelDetail.mockResolvedValue(mockPersonnel);
    deletePersonnel.mockRejectedValue(new Error(errorMessage)); // Mock delete failure

    const confirmSpy = jest.spyOn(window, 'confirm');
    confirmSpy.mockReturnValue(true); // Simulate user clicking OK

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error

    render(<PersonnelDetailScreen />);

    // Wait for the personnel details to load
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Click "Delete" button
    fireEvent.click(screen.getByText('Delete'));

    // Check if window.confirm was called
    expect(confirmSpy).toHaveBeenCalledWith('Are you sure you want to delete this personnel?');

    // Check if deletePersonnel API was called
    expect(deletePersonnel).toHaveBeenCalledWith('1');

    // Check if console.error was called with the error
    await waitFor(() => expect(consoleErrorSpy).toHaveBeenCalledWith('Error deleting personnel:', expect.any(Error)));

    consoleErrorSpy.mockRestore(); // Restore console.error
  });
});

describe('PersonnelFormScreen', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders correctly for adding new personnel', async () => {
    useParams.mockReturnValue({}); // No ID for creation
    getPersonnelDetail.mockResolvedValue(null); // No existing data for creation

    render(<PersonnelFormScreen />);

    // Wait for loading to finish (should be quick for creation)
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Check if the form title is correct
    expect(screen.getByText('Add Personnel')).toBeInTheDocument();

    // Check for input fields
    expect(screen.getByLabelText('Name:')).toBeInTheDocument();
    expect(screen.getByLabelText('Position:')).toBeInTheDocument();
    // Add checks for other input fields as needed

    // Check for buttons
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeInTheDocument();
  });

  test('renders correctly for editing existing personnel', async () => {
    const mockPersonnel = { id: '1', name: 'Jane Smith', position: 'Designer' };
    useParams.mockReturnValue({ id: '1' }); // Provide ID for editing
    getPersonnelDetail.mockResolvedValue(mockPersonnel); // Return existing data

    render(<PersonnelFormScreen />);

    // Wait for loading to finish and form to populate
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Check if the form title is correct
    expect(screen.getByText('Edit Personnel')).toBeInTheDocument();

    // Check if input fields are pre-populated with existing data
    expect(screen.getByLabelText('Name:')).toHaveValue(mockPersonnel.name);
    expect(screen.getByLabelText('Position:')).toHaveValue(mockPersonnel.position);
    // Add checks for other input fields as needed

    // Check for buttons
    expect(screen.getByRole('button', { name: 'Save' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeInTheDocument();
  });

  test('handles input changes', async () => {
    useParams.mockReturnValue({}); // Creation mode
    getPersonnelDetail.mockResolvedValue(null);

    render(<PersonnelFormScreen />);

    // Wait for loading to finish
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const nameInput = screen.getByLabelText('Name:');
    const positionInput = screen.getByLabelText('Position:');

    // Simulate typing in the name input
    fireEvent.change(nameInput, { target: { name: 'name', value: 'New Name' } });
    expect(nameInput).toHaveValue('New Name');

    // Simulate typing in the position input
    fireEvent.change(positionInput, { target: { name: 'position', value: 'New Position' } });
    expect(positionInput).toHaveValue('New Position');
  });

  test('handles form submission for creation', async () => {
    useParams.mockReturnValue({}); // Creation mode
    getPersonnelDetail.mockResolvedValue(null);
    createPersonnel.mockResolvedValue({ id: 'new-id', name: 'New Name', position: 'New Position' }); // Mock successful creation

    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    render(<PersonnelFormScreen />);

    // Wait for loading to finish
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const nameInput = screen.getByLabelText('Name:');
    const positionInput = screen.getByLabelText('Position:');
    const saveButton = screen.getByRole('button', { name: 'Save' });

    // Simulate typing
    fireEvent.change(nameInput, { target: { name: 'name', value: 'New Name' } });
    fireEvent.change(positionInput, { target: { name: 'position', value: 'New Position' } });

    // Click save
    fireEvent.click(saveButton);

    // Check if createPersonnel was called with correct data
    expect(createPersonnel).toHaveBeenCalledWith({ name: 'New Name', position: 'New Position' });

    // Wait for navigation after creation
    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/personnel')); // Assuming navigate to list after creation
  });

  test('handles form submission for update', async () => {
    const mockPersonnel = { id: '1', name: 'Jane Smith', position: 'Designer' };
    useParams.mockReturnValue({ id: '1' }); // Editing mode
    getPersonnelDetail.mockResolvedValue(mockPersonnel);
    updatePersonnel.mockResolvedValue({ id: '1', name: 'Updated Name', position: 'Updated Position' }); // Mock successful update

    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    render(<PersonnelFormScreen />);

    // Wait for loading to finish and form to populate
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const nameInput = screen.getByLabelText('Name:');
    const positionInput = screen.getByLabelText('Position:');
    const saveButton = screen.getByRole('button', { name: 'Save' });

    // Simulate typing to update
    fireEvent.change(nameInput, { target: { name: 'name', value: 'Updated Name' } });
    fireEvent.change(positionInput, { target: { name: 'position', value: 'Updated Position' } });

    // Click save
    fireEvent.click(saveButton);

    // Check if updatePersonnel was called with correct data
    expect(updatePersonnel).toHaveBeenCalledWith('1', { name: 'Updated Name', position: 'Updated Position' });

    // Wait for navigation after update
    await waitFor(() => expect(mockNavigate).toHaveBeenCalledWith('/personnel/1')); // Assuming navigate to detail after update
  });

  test('prevents submission if required fields are empty', async () => {
    useParams.mockReturnValue({}); // Creation mode
    getPersonnelDetail.mockResolvedValue(null);
    createPersonnel.mockResolvedValue({}); // Mock successful creation

    render(<PersonnelFormScreen />);

    // Wait for loading to finish
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const saveButton = screen.getByRole('button', { name: 'Save' });

    // Click save without filling fields
    fireEvent.click(saveButton);

    // Check that createPersonnel was NOT called due to validation
    expect(createPersonnel).not.toHaveBeenCalled();

  test('handles cancellation', async () => {
    useParams.mockReturnValue({}); // Creation mode
    getPersonnelDetail.mockResolvedValue(null);

    const mockNavigate = jest.fn();
    useNavigate.mockReturnValue(mockNavigate);

    render(<PersonnelFormScreen />);

    // Wait for loading to finish
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const cancelButton = screen.getByRole('button', { name: 'Cancel' });

    // Click cancel
    fireEvent.click(cancelButton);

    // Check if navigate was called
    expect(mockNavigate).toHaveBeenCalledWith('/personnel'); // Assuming navigate to list on cancel from creation

    // Test cancellation in editing mode
    useParams.mockReturnValue({ id: '1' });
    getPersonnelDetail.mockResolvedValue({ id: '1', name: 'Jane Smith', position: 'Designer' });
    mockNavigate.mockClear(); // Clear previous navigation calls

    render(<PersonnelFormScreen />);

    // Wait for loading to finish
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const cancelButtonEdit = screen.getByRole('button', { name: 'Cancel' });

    // Click cancel
    fireEvent.click(cancelButtonEdit);

    // Check if navigate was called
    expect(mockNavigate).toHaveBeenCalledWith('/personnel/1'); // Assuming navigate to detail on cancel from editing
  });

  test('displays error message if fetching personnel for editing fails', async () => {
    const errorMessage = 'Failed to fetch personnel for editing';
    useParams.mockReturnValue({ id: '1' }); // Editing mode
    getPersonnelDetail.mockRejectedValue(new Error(errorMessage));

    render(<PersonnelFormScreen />);

    // Wait for loading to finish and error message to appear
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    // Check if the error message is displayed
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });

  test('displays error message if creation fails', async () => {
    const errorMessage = 'Failed to create personnel';
    useParams.mockReturnValue({}); // Creation mode
    getPersonnelDetail.mockResolvedValue(null);
    createPersonnel.mockRejectedValue(new Error(errorMessage)); // Mock creation failure

    render(<PersonnelFormScreen />);

    // Wait for loading to finish
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const nameInput = screen.getByLabelText('Name:');
    const positionInput = screen.getByLabelText('Position:');
    const saveButton = screen.getByRole('button', { name: 'Save' });

    // Simulate typing
    fireEvent.change(nameInput, { target: { name: 'name', value: 'New Name' } });
    fireEvent.change(positionInput, { target: { name: 'position', value: 'New Position' } });

    // Click save
    fireEvent.click(saveButton);

    // Wait for submission to finish and error message to appear
    await waitFor(() => expect(screen.queryByText('Saving...')).not.toBeInTheDocument());

    // Check if the error message is displayed
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });

  test('displays error message if update fails', async () => {
    const mockPersonnel = { id: '1', name: 'Jane Smith', position: 'Designer' };
    const errorMessage = 'Failed to update personnel';
    useParams.mockReturnValue({ id: '1' }); // Editing mode
    getPersonnelDetail.mockResolvedValue(mockPersonnel);
    updatePersonnel.mockRejectedValue(new Error(errorMessage)); // Mock update failure

    render(<PersonnelFormScreen />);

    // Wait for loading to finish and form to populate
    await waitFor(() => expect(screen.queryByText('Loading...')).not.toBeInTheDocument());

    const nameInput = screen.getByLabelText('Name:');
    const positionInput = screen.getByLabelText('Position:');
    const saveButton = screen.getByRole('button', { name: 'Save' });

    // Simulate typing to update
    fireEvent.change(nameInput, { target: { name: 'name', value: 'Updated Name' } });
    fireEvent.change(positionInput, { target: { name: 'position', value: 'Updated Position' } });

    // Click save
    fireEvent.click(saveButton);

    // Wait for submission to finish and error message to appear
    await waitFor(() => expect(screen.queryByText('Saving...')).not.toBeInTheDocument());

    // Check if the error message is displayed
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });
});

  // TODO: Add tests for navigation/cancellation
  // TODO: Add tests for error states (fetching and submission)
});
