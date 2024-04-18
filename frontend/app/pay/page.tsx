'use client'
import React, { useState, useEffect } from 'react';
import DynamicSingleSelectDropdown from '../components/singleDropdown/dynamicSingleSelectDropdown'; 

import React, { useState } from 'react';


const Pay: React.FC = () => {
  const [formData, setFormData] = useState({
    amount: '',
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

  const handleSelect = (value: string | number) => {
    setSelectedOption(value);
  }

  return (
    <div className='container'>
      <h1 className='payReqTitle'>Let's Pay!</h1>
      <form onSubmit={handleSubmit} className="form">
      <div className='form-group'>
      <label htmlFor="amount" className="amount">
            $:
          </label>
          <input
            type="text"
            id="amount"
            name="amount"
            value={formData.amount}
            onChange={handleChange}
            className="input"
            placeholder=" "
            required
          />
      </div>
        <div className="form-group">
          <label htmlFor="payTo" className="payTo">
            To:
          </label>
          <input
            type="text"
            id="payTo"
            name="payTo"
            value={formData.payTo}
            onChange={handleChange}
            className="input"
            placeholder="Username"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="msg" className="msg">
            Message:
          </label>
          <input
            type="text"
            id="msg"
            name="msg"
            value={formData.msg}
            onChange={handleChange}
            className="input"
            placeholder="What's this for?"
            required
          />
        </div>
      </form>
      <div className='payReqButtons'>
      <DynamicSingleSelectDropdown options={householdUsers} label="Select User" onSelect={handleSelect} />
        <button className='payReqButton w-full'>Pay</button>
      </div>
    </div>
  );
};

export default Pay;
