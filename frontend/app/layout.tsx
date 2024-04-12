import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./styles/globals.css";
import React from 'react';
import Navigation from "./components/navigation/navigationBar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PayArray",
  description: "Split costs with your rommates effortlessly",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navigation />
        {children}
      </body>
    </html>
  );
}

