'use client'
import { useState } from 'react'

const Pay: React.FC = () => {
    return (
        /*need some input tag for money, need to input area, reason input area*/
        <div className = 'container'>
            <h1 className= 'payReqTitle'>Pay and Request</h1>
        <div className='moneyAmount'>
            <p>$</p>
        </div>
        <div className= 'payReqButtons'>
        <button className= 'payReqButton w-full'>Pay</button>
        <button className= 'payReqButton w-full'>Request</button>
        </div>
        
        </div>
        

      );
    }
    
  
  export default Pay;