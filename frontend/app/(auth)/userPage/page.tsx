'use client'
import { useState } from 'react'
import Link from 'next/link';


const UserLandingPage: React.FC = () => {
    const [formData, setFormData] = useState({
      email: '',
      username: '',
      password: '',
      confirmPassword: '',
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
      <div className="container">
      <div className="sidebar">
          <h1 className="helloUsername">Hello {formData.username}!</h1>
          <div className="userButtonGroup">
            <Link href= "/payRequest">
            <button className="userButton w-full">Pay or Request</button>
            </Link>
              <button className="userButton w-full">My Household</button>
              <button className="userButton w-full">My Budget</button>
          </div>
      </div>
      <div className="transactionContent">
        <h1 className= "transactionTitle">Transactions</h1>
          
      </div>
  </div>
        
      );
    };
  
  export default UserLandingPage;