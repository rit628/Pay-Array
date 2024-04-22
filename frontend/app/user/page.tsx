'use client'
import { useState } from 'react'
import Link from 'next/link';


const UserLandingPage: React.FC = () => {
    return (
      <div className="container">
      <div className="sidebar">
          <h1 className="helloUsername">Hello {localStorage.getItem('username')}!</h1>
          <div className="userButtonGroup">
            <Link href= "/pay">
            <button className="userButton w-full">Pay</button>
            </Link>
            <Link href= "/request">
            <button className="userButton w-full">Request</button>
            </Link>
          </div>
      </div>
      <div className="transactionContent">
        <h1 className= "transactionTitle">Transactions</h1>
          
      </div>
  </div>
        
      );
    };
  
  export default UserLandingPage;