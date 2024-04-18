'use client'
import React, { useState } from 'react';

import React, { useState } from 'react';


const Pay: React.FC = () => {
  const [formData, setFormData] = useState({
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
      <div className='payReqButtons'>
        <button className='payReqButton w-full'>Pay</button>
      </div>
    </div>
  );
};

export default Pay;
