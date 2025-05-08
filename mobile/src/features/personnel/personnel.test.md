# Tests for Mobile Frontend Personnel Feature

This document outlines the tests that should be implemented for the Mobile Frontend Personnel feature.

## PersonnelListScreen Tests:
- [ ] Should render the list of personnel.
- [ ] Should navigate to PersonnelDetailScreen when a personnel item is pressed.
- [ ] Should navigate to PersonnelFormScreen when the "Add Personnel" button is pressed.

## PersonnelDetailScreen Tests:
- [ ] Should render personnel details when a valid ID is provided.
- [ ] Should display "Personnel not found" when an invalid ID is provided.

## PersonnelFormScreen Tests:
- [ ] Should render input fields for personnel details.
- [ ] Should pre-populate form fields when editing existing personnel.
- [ ] Should call the createPersonnel API when saving a new personnel.
- [ ] Should call the updatePersonnel API when saving an existing personnel.
- [ ] Should navigate back after successful save.

## personnelApi.js Tests:
- [ ] Should test the `getAllPersonnel` function (simulated or actual API call).
- [ ] Should test the `getPersonnelById` function (simulated or actual API call).
- [ ] Should test the `createPersonnel` function (simulated or actual API call).
- [ ] Should test the `updatePersonnel` function (simulated or actual API call).
- [ ] Should test the `deletePersonnel` function (simulated or actual API call).
