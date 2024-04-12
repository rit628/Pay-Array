import Head from "next/head";
import Navigation from "../components/navigationBar";

const Home = () => {
  return (
    <>
      <Head>
        <title>PayArray | Home</title>
      </Head>
      <Navigation />
        <div className="container">
          <h1>Home</h1>
          <p>Split costs with your rommates effortlessly</p>
        </div>
    </>
  );
};

export default Home;
