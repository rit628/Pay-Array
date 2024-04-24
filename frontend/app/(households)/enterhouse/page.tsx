'use client'
import { useState } from 'react'
import * as React from 'react';
import { useRouter } from 'next/navigation';

const EnterHouse: React.FC = () => {
    const router = useRouter();
    const prepopulatedId = localStorage.getItem("household-id-temp");
    localStorage.removeItem("household-id-temp");
    const [formData, setFormData] = useState({
      houseCode: (prepopulatedId) ? prepopulatedId : '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
      };
    
      const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        const header : any = localStorage.getItem('auth-header');
        const response = await fetch(`${process.env.API_URL}/users/me/household_id/`, {
          "method": "POST",
          "mode": "cors",
          "headers": {
            "Content-Type": "application/json",
            "Authorization": header
          },
          "body": JSON.stringify(formData.houseCode)
        });
        await response.json();
        if (response.ok) {
          router.push("/user");
        }
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