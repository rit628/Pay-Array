import Head from "next/head";
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import Link from 'next/link'

const OpenScreen = () => {
  return (
    <div className="container">
      <Head>
        <title>PayArray</title>
      </Head>
      <h1>PayArray</h1>
      <p>Split costs with your roomates effortlessly</p>
      <div className="page-container">
        <Link href="signup"><button type="submit" className="submit-button">Sign Up</button></Link>
        <Link href="login"><button type="submit" className="submit-button">Log In</button></Link>
      </div>
      <br></br>
      <br></br>
      <h2>Features</h2>
      <div className="info">
      <Card className="card">
          <p>Easily split expenses with your rooommates using PayArray! With us, you'll be able to easily create households and evenly request and pay costs between your group members hassle-free.</p>
      </Card>
      <Card className="card">Managing your shared expenses has never been easier or safer with PayArray. Keep track of your household costs with us!</Card>
      </div>
    </div>
  );
};

export default OpenScreen;