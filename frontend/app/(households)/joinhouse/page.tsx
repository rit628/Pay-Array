'use client'
import Head from "next/head";
import Link from 'next/link';
import Button from '@mui/material/Button';
import { useState, useEffect } from "react";

const JoinHouse = () => {
  const [householdId, setHouseholdId] = useState(null);

  const createHousehold = async () => {
    const response = await fetch(`${process.env.API_URL}/users/household/create/`, {
      "method": "POST",
      "mode": "cors",
      "headers": {
        "Content-Type": "application/json",
      },
    });
    const householdId = await response.json();
    setHouseholdId(householdId);
    localStorage.setItem("household-id-temp", householdId);
  };


  return (
    <div className="container">
      <Head>
        <title>Join Household | PayArray</title>
      </Head>
      <h1>Join a Household</h1>
      <p>Split costs hassle-free!</p>
      <div className="button-container">
        {!householdId && <Button className="submit-button" onClick={createHousehold}>Create a Household</Button>}
        {householdId && <div>Your household id is: {householdId}.</div>}
        <Link href="/enterhouse" legacyBehavior>
            <Button className="submit-button">{ (householdId) ? "Join" : "Enter House Code"}</Button>
        </Link>
      </div>
    </div>
  );
};

export default JoinHouse;