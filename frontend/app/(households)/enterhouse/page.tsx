'use client'
import { useState } from 'react'
import * as React from 'react';

const EnterHouse: React.FC = () => {
    const [formData, setFormData] = useState({
      houseCode: '',
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
      <>
      <title>Enter Household | PayArray</title>
        <div className="container">
        <div className="login-container">
            <h2 className="title">Join an Existing Household</h2>
            <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label htmlFor="houseCode" className="label">
                  House Code:
                </label>
                <input
                  type="houseCode"
                  id="houseCode"
                  name="houseCode"
                  value={formData.houseCode}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your House Code"
                  required
                />
              </div>
              <button type="submit" className="submit-button">Join</button>
            </form>
          </div>
        </div>
        </>
      );
    };
  
  export default EnterHouse;