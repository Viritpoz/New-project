import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/navbar/index';
const IndexLayout: React.FC = () => {
  return (
    <div className="flex flex-col h-screen bg-black text-white">
      <Navbar></Navbar>
      <div className="flex-grow">
      <Outlet/>
      </div>
    </div>
  );
}
export default IndexLayout;