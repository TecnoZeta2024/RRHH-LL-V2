import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';

const PersonnelFormScreen = ({ route, navigation }) => {
  const { personnelId } = route.params || {}; // Get personnelId if editing

  const [name, setName] = useState('');
  const [title, setTitle] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    if (personnelId) {
      // In a real application, fetch personnel data for editing
      const dummyPersonnelData = {
        '1': { name: 'John Doe', title: 'Field Worker', phone: '123-456-7890', email: 'john.doe@example.com' },
        '2': { name: 'Jane Smith', title: 'Supervisor', phone: '987-654-3210', email: 'jane.smith@example.com' },
        '3': { name: 'Peter Jones', title: 'Field Worker', phone: '555-123-4567', email: 'peter.jones@example.com' },
      };
      const personnel = dummyPersonnelData[personnelId];
      if (personnel) {
        setName(personnel.name);
        setTitle(personnel.title);
        setPhone(personnel.phone);
        setEmail(personnel.email);
      }
    }
  }, [personnelId]);

  const handleSave = () => {
    // In a real application, send data to the backend API
    const personnelData = { name, title, phone, email };
    console.log('Saving personnel data:', personnelData);
    navigation.goBack(); // Go back after saving
  };

  return (
    <View style={styles.container}>
      <Text style={styles.label}>Name:</Text>
      <TextInput style={styles.input} value={name} onChangeText={setName} />

      <Text style={styles.label}>Title:</Text>
      <TextInput style={styles.input} value={title} onChangeText={setTitle} />

      <Text style={styles.label}>Phone:</Text>
      <TextInput style={styles.input} value={phone} onChangeText={setPhone} keyboardType="phone-pad" />

      <Text style={styles.label}>Email:</Text>
      <TextInput style={styles.input} value={email} onChangeText={setEmail} keyboardType="email-address" />

      <Button title="Save" onPress={handleSave} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 20,
    paddingHorizontal: 10,
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 15,
    borderRadius: 5,
  },
});

export default PersonnelFormScreen;
