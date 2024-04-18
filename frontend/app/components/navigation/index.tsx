// App.tsx
import React from "react";
import Navbar from "./navigationBar";
import Household from "../../household/page"
import User from "../../user/page";

export default function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Household />
        <User />
      </div>
    </>
  );
}
