'use client'
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import Card from '@mui/material/Card' 

const Household = () => {
  const router = useRouter();
  const [householdId, setHouseholdId] = useState(null);
  const [householdMembers, setHouseholdMembers] = useState<Array<any>>([1, 2, 3]);
  const header : any = localStorage.getItem('auth-header');
  useEffect(() => {
    const fetchHouseholdMembers = async () => {
      try {
        const header: any = localStorage.getItem('auth-header');
        if (header === null) {
          router.push("/");
        }
        const response = await fetch(`${process.env.API_URL}/users/me/household/`, {
          method: 'GET',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': header
          }
        });
        const data = await response.json();
        
        setHouseholdMembers(data);
      } catch (error) {
        console.error('Error fetching Household members:', error);
      }
    };
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
      if (!response.ok) {
        router.push("/");
      }
      setHouseholdId(householdId);
    };
    getHouseholdId();
    fetchHouseholdMembers();
  }, []);
  return (
    <div className='container'>
      <div className="transactionContent">        
        <h1 className="transactionTitle">Other Users in Household {householdId}:</h1>
        <ul>
          {householdMembers.map((member, index) => (
            <li key={index}>
              <Card className="card" >
              <div>
                <strong>Username: </strong> {member.username}
              </div>
              </Card>
            </li>
          ))}
        </ul>
        </div>
    </div>
  );
  
    }
    
  
  export default Household;