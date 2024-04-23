'use client'
import { useState, useEffect } from "react"; 

const Household = () => {

  const [householdId, setHouseholdId] = useState(null);
  const header : any = localStorage.getItem('auth-header');
  useEffect(() => {
    const getHouseholdId = async () => {
      const response = await fetch(`${process.env.API_URL}/users/me/household_id/`, {
        "method": "GET",
        "mode": "cors",
        "headers": {
          "Content-Type": "application/json",
          "Authorization": header
        },
      });
      const householdId = await response.json();
      setHouseholdId(householdId);
    };
    getHouseholdId();
  }, []);
    return (
       <div className='container'>
        <p className='householdTitle'>Your Household: {householdId}</p>
       </div>
        

      );
    }
    
  
  export default Household;