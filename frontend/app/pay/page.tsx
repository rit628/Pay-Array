'use client'
import React, { useState, useEffect } from 'react';
import DynamicSingleSelectDropdown from '../components/singleDropdown/dynamicSingleSelectDropdown'; 


const Pay: React.FC = () => {
  const [formData, setFormData] = useState({
    payTo: '',
    msg: '',
  });

  // State to hold household users
  const [householdUsers, setHouseholdUsers] = useState([]);

  // Function to fetch household users
  const getHouseholdUsers = async () => {
    try {
      const header = localStorage.getItem("auth-header")|| '';
      const response = await fetch(`${process.env.API_URL}/users/me/household_id`, {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Authorization": header
        }
      });

      const userHouseholdId = await response.json();

      const response2 = await fetch(`${process.env.API_URL}/users/household/${userHouseholdId}`, {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          "Authorization": header
        }
      });

      const householdUsers = await response2.json();
      setHouseholdUsers(householdUsers);
    } catch (error) {
      console.error("Error fetching household users:", error);
    }
  };

  useEffect(() => {
    // erm
    getHouseholdUsers();
  }, []); 

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

  return (
    <div className='container'>
      <h1 className='payReqTitle'>Let's Pay!</h1>
      <div className='payReqButtons'>
      <DynamicSingleSelectDropdown options={householdUsers} label="Select User" />
        <button className='payReqButton w-full'>Pay</button>
      </div>
    </div>
  );
};

export default Pay;
