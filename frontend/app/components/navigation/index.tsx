// App.tsx
import React from "react";
import Navbar from "./navigationBar";
import Home from "../../home/page";
import Landing from "../../landing/page";
import Profile from "../../profile/page";

export default function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Home />
        <Landing />
        <Profile />
      </div>
    </>
  );
}
