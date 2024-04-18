import Head from "next/head";
import Link from 'next/link';
import Button from '@mui/material/Button';

const JoinHouse = () => {
  return (
    <div className="container">
      <Head>
        <title>Join Household | PayArray</title>
      </Head>
      <h1>Join a Household</h1>
      <p>there is some quick blurb here</p>
      <div className="button-container">
        <Link href="/createhouse" legacyBehavior>
          <Button className="submit-button">Create a Household</Button>
        </Link>
        <Link href="/enterhouse" legacyBehavior>
            <Button className="submit-button">Enter House Code</Button>
        </Link>
      </div>
    </div>
  );
};

export default JoinHouse;
