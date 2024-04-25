'use client'
import React, { useState, useEffect } from 'react';
import DynamicSingleSelectDropdown from '../components/userDropdown/userSelectDropdown'; 
import TransactionDropdown from '../components/transactionDropdown/transactionDropdown'; 
import { useRouter } from 'next/navigation';



const Pay: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    payTo: '',
    msg: '',
  });

  // States
  const [householdUsers, setHouseholdUsers] = useState([]);
  const[transactions, setTransactions] = useState<any>([]);
  const [selectedOption, setSelectedOption] = useState<string | number>('');
  const [selectedTransaction, setSelectedTransaction] = useState<string | number>('');
  const [transactionList, setTransactionList] = useState<any>([]);
  const [brokeFlag, setBrokeFlag] = useState(false);



  // Function to fetch household users
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
        
        setHouseholdUsers(data)
      }
    }
    fetchHouseholdUsers();
  }, [])

  useEffect(() => {
    const fetchTransactions = async () => {
      const header : any = localStorage.getItem('auth-header');
      const response = await fetch(`${process.env.API_URL}/users/me/transactions/due/`, {
        "method": "GET",
        "mode": "cors",
        "headers": {
          "Content-Type": "application/json",
          "Authorization": header
        },
      });
      const data = await response.json();
      if (response.ok) {
        
        setTransactionList(data);
      }
    }
    fetchTransactions();

  }, [])

  // Handle form change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    const header : any = localStorage.getItem("auth-header");
    try {
      const response = await fetch(`${process.env.API_URL}/users/me/transactions/${selectedTransaction}/pay/`, {
        "method": "POST",
        "mode": "cors",
        "headers": {
          "Content-Type": "application/json",
          "Authorization": header
        },
      });
      const data = await response.json();
      
      router.push("/user");
    } catch (error) {
      setBrokeFlag(true);
    }
  };


  const handleSelect = async (value: string | number | (string | number)[]) => {
    if (Array.isArray(value)) {
      console.log('multiselect error on pay');
    } else {
      // single-select case
      setSelectedOption(value);
      const fetchFilteredTransactions = async () => {
        if (!transactionList) {
          return;
        }
        let userTransactions : any = [];

        transactionList.forEach(transaction => {
          if (transaction.purchaser === value) {
            userTransactions.push(transaction);
          }
        });
        // const userTransactions = transactionList.filter((transaction: { purchaser: string | number; }) => transaction.purchaser === selectedOption);
        setTransactions(userTransactions);
        
      }
    
      await fetchFilteredTransactions();
    }
  };
  const handleSelectedTransaction = (value: string | number | (string | number)[]) => {
    if (Array.isArray(value)) {
      console.log('multiselect error on pay');
    } else {
      // single-select case
      setSelectedTransaction(value);
    }
  };

        {/* still need to set selected transaction as paid */}


  return (
    <div className='container'>
      <h1 className='payReqTitle'>Let's Pay!</h1>
      <div className='payReqButtons' style={{width: '30%'}}>
      <DynamicSingleSelectDropdown options={householdUsers} label="Select User" onSelect={handleSelect} multiSelect={false} />
      <TransactionDropdown options={transactions} label="Select Transaction" onSelect={handleSelectedTransaction} multiSelect={false}/>
      {/* still need to set selected transaction as paid */}

        {brokeFlag && <div>You Broke!</div>}
        <button className='payReqButton w-full' onClick={handleSubmit}>Pay</button>
      </div>
    </div>
  );
};

export default Pay;