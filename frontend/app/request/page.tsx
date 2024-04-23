'use client'
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import DynamicSingleSelectDropdown from '../components/singleDropdown/dynamicSingleSelectDropdown';


const Pay: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    amount: '',
    users: [],
    message: '',
  });

  const [householdUsers, setHouseholdUsers] = useState([]);

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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);
    const header : any = localStorage.getItem('auth-header');
    const response = await fetch(`${process.env.API_URL}/users/me/transactions/`, {
      "method": "POST",
      "mode": "cors",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": header
      },
      "body": JSON.stringify(formData)
    });
    await response.json();
    if (response.ok) {
      router.push("/user");
    }
  };

  return (
    <div className='container'>
      <h1 className='payReqTitle'>Send a Request!</h1>
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
          <label htmlFor="users" className="users">
            To:
          </label>
          <DynamicSingleSelectDropdown label="Who are you sending the request to?" options={householdUsers}></DynamicSingleSelectDropdown>
        </div>
        <div className="form-group">
          <label htmlFor="message" className="message">
            Message:
          </label>
          <input
            type="text"
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            className="input"
            placeholder="What's this for?"
            required
          />
        </div>
      <div className='payReqButtons'>
        <button type="submit" className='payReqButton w-full'>Send Request</button>
      </div>
      </form>
    </div>
  );
};

export default Pay;