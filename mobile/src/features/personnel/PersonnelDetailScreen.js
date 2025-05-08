import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const PersonnelDetailScreen = ({ route }) => {
  const { personnelId } = route.params;

  // In a real application, you would fetch personnel details using personnelId
  const dummyPersonnelDetails = {
    '1': { name: 'John Doe', title: 'Field Worker', phone: '123-456-7890', email: 'john.doe@example.com' },
    '2': { name: 'Jane Smith', title: 'Supervisor', phone: '987-654-3210', email: 'jane.smith@example.com' },
    '3': { name: 'Peter Jones', title: 'Field Worker', phone: '555-123-4567', email: 'peter.jones@example.com' },
  };

  const personnel = dummyPersonnelDetails[personnelId];

  if (!personnel) {
    return (
      <View style={styles.container}>
        <Text>Personnel not found</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.name}>{personnel.name}</Text>
      <Text style={styles.title}>{personnel.title}</Text>
      <Text>Phone: {personnel.phone}</Text>
      <Text>Email: {personnel.email}</Text>
      {/* Add more details as needed */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 20,
    paddingHorizontal: 10,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  title: {
    fontSize: 18,
    color: '#666',
    marginBottom: 20,
  },
});

export default PersonnelDetailScreen;
