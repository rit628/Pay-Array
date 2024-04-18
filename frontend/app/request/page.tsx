import Head from "next/head";

const Request = () => {
  return (
        /*need some input tag for money, need to input area, reason input area*/
        <div className = 'container'>
            <h1 className= 'payReqTitle'>Let's Request!</h1>
        <div className='moneyAmount'>
            <p>$</p>
        </div>
        <div className= 'payReqButtons'>
        <button className= 'payReqButton w-full'>Request</button>
        </div>
        </div>
  );
};

export default Request;
