import Head from "next/head";
import Navigation from "../components/navigation/navigationBar";

const Home = () => {
  return (
    <>
      <Head>
        <title>PayArray | Home</title>
      </Head>
        <div className="container">
          <h1>Home</h1>
          <p>Split costs with your rommates effortlessly</p>
        </div>
    </>
  );
};

export default Home;
