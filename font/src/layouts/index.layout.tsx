import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/navbar/index';
import Loading from '../components/loading';
import { SNMP } from '../interfaces/snmp.interface';
const IndexLayout: React.FC<{loading:boolean,snmpData: SNMP | null,setLoading:React.Dispatch<React.SetStateAction<boolean>>}> = ({loading,snmpData,setLoading}) => {
  return (<>
    <div className="flex flex-col h-screen bg-black text-white">
      {loading ? <Loading/> : <>
      <Navbar snmpData={snmpData} setLoading={setLoading}></Navbar>
      <div className="flex-grow">
      <Outlet/>
      </div>
      </> }
    </div>
  </>
  );
}
export default IndexLayout;