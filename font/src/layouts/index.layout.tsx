import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/navbar/index';
import Loading from '../components/loading';
const IndexLayout: React.FC<{loading:boolean}> = ({loading}) => {
  return (<>
    <div className="flex flex-col h-screen bg-black text-white">
      {loading ? <Loading/> : <>
      <Navbar></Navbar>
      <div className="flex-grow">
      <Outlet/>
      </div>
      </> }
    </div>
  </>
  );
}
export default IndexLayout;