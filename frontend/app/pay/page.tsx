'use client'
import React, { useState, useEffect } from 'react';
import DynamicSingleSelectDropdown from '../components/userDropdown/userSelectDropdown'; 


const Pay: React.FC = () => {
  const [formData, setFormData] = useState({
    payTo: '',
    msg: '',
  });

  // State to hold household users
  const [householdUsers, setHouseholdUsers] = useState([]);

  // Function to fetch household users
  useEffect(() => {
    const fetchHouseholdUsers = async () => {
      const header : any = localStorage.getItem('auth-header');
      const response = await fetch(`${process.env.API_URL}/users/me/household/`, {
        "method": "GET",
        "mode": "cors",
        "headers": {
          "Content-Type": "application/json",
          "Authorization": header
        },
      });
      const data = await response.json();
      if (response.ok) {
        console.log(data);
        setHouseholdUsers(data)
      }
    }
    fetchHouseholdUsers();
  }, [])

  // Handle form change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);
    // logic
  };

  const [selectedOption, setSelectedOption] = useState<string | number>('');

  const handleSelect = (value: string | number | (string | number)[]) => {
    if (Array.isArray(value)) {
      console.log('multiselect error on pay');
    } else {
      // single-select case
      setSelectedOption(value);
    }
  };

  return (
    <div className='container'>
      <h1 className='payReqTitle'>Let's Pay!</h1>
      <div className='payReqButtons'>
      <DynamicSingleSelectDropdown options={householdUsers} label="Select User" onSelect={handleSelect} multiSelect={false} />
        <button className='payReqButton w-full'>Pay</button>
      </div>
    </div>
  );
};

export default Pay;
