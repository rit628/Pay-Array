'use client'
import React, { useState } from 'react';

import React, { useState } from 'react';


const Pay: React.FC = () => {
  const [formData, setFormData] = useState({
    amount: '',
    payTo: '',
    msg: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);
    // logic
  };

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
        <button className='payReqButton w-full'>Pay</button>
      </div>
    </div>
  );
};

export default Pay;
