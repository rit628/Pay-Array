import React, { useState } from 'react';
import { Select, MenuItem, FormControl, InputLabel, SelectChangeEvent } from '@mui/material';

interface Option {
 //   transaction objects
  amount: number
  message : string
  id : number
}

interface Props {
  options: Option[];
  label: string;
  onSelect: (value: string | number | (string | number)[]) => void;
  multiSelect?: boolean; // Optional multi-select prop
}

const TransactionDropdown: React.FC<Props> = ({ options, label, onSelect, multiSelect = false }) => {
  const [selectedOptions, setSelectedOptions] = useState<(string | number)[]>([]); // State to hold selected options

  const handleChange = (event: SelectChangeEvent<(string | number) | (string | number)[]>) => {
    const selectedValue = event.target.value;
    setSelectedOptions(Array.isArray(selectedValue) ? selectedValue : [selectedValue]);
    onSelect(selectedValue);
  };

  return (
    <FormControl fullWidth>
      <InputLabel id="dynamic-select-label">{label}</InputLabel>
      <Select
        labelId="dynamic-select-label"
        id="dynamic-select"
        value={multiSelect ? selectedOptions : selectedOptions[0] || ''} // Handle multi-select vs single-select
        onChange={handleChange}
        multiple={multiSelect} // Set multiple attribute based on multiSelect prop
      >
        <MenuItem value="" disabled>
          {label}
        </MenuItem>
        {options.map((option) => (
          <MenuItem key={option.id} value={option.id}>
                {`${option.amount} - ${option.message}`}

          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default TransactionDropdown;
