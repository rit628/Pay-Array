'use client'
import React, { useState, useEffect } from 'react';
import Link from 'next/link';


const UserLandingPage: React.FC = () => {
  const [transactions, setTransactions] = useState<Array<any>>([1, 2]);
  const [user, setUser] = useState<any>();

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const header: any = localStorage.getItem('auth-header');
        const response = await fetch(`${process.env.API_URL}/users/me/transactions/due/`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': header
          }
        });
        const data = await response.json();
        setTransactions(data);
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
        setUser(data);
      } catch (error) {
        console.error('Error fetching User:', error);
      }
    };
    fetchTransactions();
    fetchUser();
  }, []);
  
  return (
    <div className="container">
      <div className="sidebar">
        <h1 className="helloUsername">Hello {user?.username}!</h1>
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
        <h1 className="transactionTitle">Transactions:</h1>
        <ul>
          {transactions.map((transaction, index) => (
            <li key={index}>
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
          ))}
        </ul>
      </div>
    </div>
  );
};

export default UserLandingPage;
