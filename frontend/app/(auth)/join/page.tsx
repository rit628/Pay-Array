import Head from "next/head";
import Link from 'next/link';

const Join = () => {
  return (
    <div className="container">
      <Head>
        <title>PayArray</title>
      </Head>
      <h1>PayArray</h1>
      <p>Split costs with your roommates effortlessly</p>
      <div className="button-container">
        <Link href="/signup" legacyBehavior>
          <button className="button">Sign Up</button>
        </Link>
        <Link href="/login" legacyBehavior>
          <button className="button">Login</button>
        </Link>
      </div>
    </div>
  );
};

export default Join;
