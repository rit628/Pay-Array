import Head from "next/head";
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'

const OpenScreen = () => {
  return (
    <div className="container">
      <Head>
        <title>PayArray</title>
      </Head>
      <h1>PayArray</h1>
      <p>Split costs with your rommates effortlessly</p>
      <h2>Features</h2>
      <div className="info">
      <Card className="card">Test</Card>
      <Card className="card">Another Test</Card>
      <Card className="card">More Tests</Card>
      </div>
    </div>
  );
};

export default OpenScreen;
