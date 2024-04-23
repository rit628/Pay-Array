import React, { useState } from 'react';
import { Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';

interface Option {
  id: number;
  username: string;
}

interface Props {
  options: Option[];
  label: string;
}

const DynamicSingleSelectDropdown: React.FC<Props> = ({ options, label }) => {
  const [selectedOption, setSelectedOption] = useState<string>(''); // selected option is a username

  const handleChange = (event: SelectChangeEvent<string>) => {
    setSelectedOption(event.target.value); 
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
          <MenuItem key={option.id} value={option.username}>
            {option.username}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default DynamicSingleSelectDropdown;
