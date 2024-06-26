'use client'
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Card from '@mui/material/Card' 


const UserLandingPage: React.FC = () => {
  const [transactions, setTransactions] = useState<Array<any>>([]);
  const [duetransactions, setDueTransactions] = useState<Array<any>>([]);
  const [user, setUser] = useState<any>();
  const router = useRouter();

  const [userData, setUserData] = useState({
    email: '',
    household_id: '',
    first_name : '',
    last_name : '',
    phone : '',
    balance : '',
    password : '',
    confirmPassword : '' as any
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUserData({ ...userData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (userData.confirmPassword != userData.password) {
      return;
    }
    let payload = userData;
    delete payload.confirmPassword;
    const header : any = localStorage.getItem('auth-header');
    let response = await fetch(`${process.env.API_URL}/users/me/`, {
      "method": "POST",
      "mode": "cors",
      "headers": {
        "Content-Type": "application/json",
        "Authorization" : header
      },
      "body": JSON.stringify(userData)
    })

    let data = await response.json();
    
  };

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const header: any = localStorage.getItem('auth-header');
        if (header === null) {
          router.push("/");
        }
        const response2 = await fetch(`${process.env.API_URL}/users/me/username/`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': header
          }
        });
        const username = await response2.json();
        const response = await fetch(`${process.env.API_URL}/users/me/transactions/`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': header
          }
        });

        const data = await response.json();
        
        let t2 : any = []
        data.forEach(t => {
          if (t.purchaser === username) {
            t2.push(t)
          }
        });
        setTransactions(t2);
      } catch (error) {
        console.error('Error fetching Transactions:', error);
      }
    };
    const fetchDueTransactions = async () => {
      try {
        const header: any = localStorage.getItem('auth-header');
        if (header === null) {
          router.push("/");
        }
        const response = await fetch(`${process.env.API_URL}/users/me/transactions/due/`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': header
          }
        });
        const data = await response.json();
        
        setDueTransactions(data);
      } catch (error) {
        console.error('Error fetching Transactions:', error);
      }
    };
    const fetchUser = async () => {
      try {
        const header: any = localStorage.getItem('auth-header');
        const response = await fetch(`${process.env.API_URL}/users/me/`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': header
          }
        });
        const data = await response.json();
        setUserData(data);
        
        setUser(data);
      } catch (error) {
        console.error('Error fetching User:', error);
      }
    };
    fetchUser();
    fetchDueTransactions();
    fetchTransactions();
  }, []);
  
  return (
    <div className="container">
      <div className="sidebar">
        <h1 className="helloUsername">Hello {user?.username}!</h1>
        <form onSubmit={handleSubmit} className="form">
              <div className="form-group">
                <label htmlFor="email" className="label">
                  Email:
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={userData.email}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your Email"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="first_name" className="label">
                  First Name:
                </label>
                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  value={userData.first_name}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your First Name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="last_name" className="label">
                  Last Name:
                </label>
                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  value={userData.last_name}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your Last Name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="phone" className="label">
                  Phone:
                </label>
                <input
                  type="text"
                  id="phone"
                  name="phone"
                  value={userData.phone}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your Phone Number"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="balance" className="label">
                  Balance:
                </label>
                <input
                  type="number"
                  id="balance"
                  name="balance"
                  value={userData.balance}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your Balance in USD"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="password" className="label">
                  Password:
                </label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={userData.password}
                  onChange={handleChange}
                  className="input"
                  placeholder="Enter your password"
                />
              </div>
              <div className="form-group">
                <label htmlFor="confirmPassword" className="label">
                  Confirm Password:
                </label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={userData.confirmPassword}
                  onChange={handleChange}
                  className="input"
                  placeholder="Confirm your password"
                />
              </div>
              <button type="submit" className="submit-button">Update Profile</button>
            </form>
          <br />
          <br />
        <div className="userButtonGroup">
          <Link href="/pay">
            <button className="userButton w-full">Pay</button>
          </Link>
          <Link href="/request">
            <button className="userButton w-full">Request</button>
          </Link>
        </div>
      </div>
      <div className="transactionContent">
        <h1 className="transactionTitle">Payments You Owe to Others</h1>
        <ul>
          {duetransactions.map((duetransaction, index) => (
            <Card className="card" style={{ backgroundColor: '#ECB3AC' }}>
            <li key={index} style={{color: 'black'}}>
              <div>
                <strong>Amount:</strong> {duetransaction.amount}
              </div>
              <div>
                <strong>Message:</strong> {duetransaction.message}
              </div>
              <div>
                <strong>Item ID:</strong> {duetransaction.item_id}
              </div>
            </li>
            </Card>
          ))}
        </ul>
        <h1 className="transactionTitle">Requests to Others</h1>
        <ul>
          {transactions.map((transaction, index) => (
            <Card className="card" style={{ backgroundColor: '#CDE8B0' }}>
            <li key={index} style={{color: 'black'}}>
              <div>
                <strong>Amount:</strong> {transaction.amount}
              </div>
              <div>
                <strong>Message:</strong> {transaction.message}
              </div>
              <div>
                <strong>Item ID:</strong> {transaction.item_id}
              </div>
            </li>
            </Card>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default UserLandingPage;