import React, { useState } from 'react';
import { Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';

interface Option {
  username : string;
  email : string;
  household_id : number;
  first_name : string;
  last_name : string;
  phone : string;
  balance : number;

}

interface Props {
  options: Option[];
  label: string;
  onSelect: (value: string | number) => void; // Callback function to handle selected value
}

const DynamicSingleSelectDropdown: React.FC<Props> = ({ options, label, onSelect }) => {
  const [selectedOption, setSelectedOption] = useState<string | number>(''); // State type can be string or number

  const handleChange = (event: SelectChangeEvent<string | number>) => {
    const selectedValue = event.target.value;
    setSelectedOption(selectedValue);
    onSelect(selectedValue); // Call the callback function with the selected option
  };

  return (
    <FormControl fullWidth>
      <InputLabel id="dynamic-select-label">{label}</InputLabel>
      <Select
        labelId="dynamic-select-label"
        id="dynamic-select"
        value={selectedOption}
        onChange={handleChange}
      >
        <MenuItem value="" disabled>
          {label} {/* Display the label for the dropdown */}
        </MenuItem>
        {options.map((option) => (
          <MenuItem key={option.email} value={option.username}>
            {option.username}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default DynamicSingleSelectDropdown;
