import Head from "next/head";
import Link from 'next/link';

const Home = () => {
  return (
    <div className="container">
      <Head>
        <title>PayArray</title>
      </Head>
      <h1>PayArray</h1>
      <p>Split costs with your rommates effortlessly</p>
      <div className="button-container">
        <Link href="/signup">
          <button className="button">Sign Up</button>
        </Link>
        <Link href="/login">
          <button className="button">Login</button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
