import React from 'react';
import { useNavigate } from "react-router-dom";
import indexRoutes from '../index';
import { SNMP } from '../../interfaces/snmp.interface';
interface NavbarProps {
  snmpData: SNMP | null;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const Navbar: React.FC<NavbarProps> = ({ snmpData, setLoading }) => {
 const indexRoute = indexRoutes(snmpData,setLoading);
 const navigate = useNavigate();
 
  return (
    <div className=' flex  w-screen bg-white rounded-full text-black p-2    '>
      <div className='flex space-x-5 ml-4'>
      <h1>Navbar</h1>
      {
        indexRoute.map((route,index)=>(
          <button  key={index} id={`${index}`}  onClick={()=>navigate(`${route.path}`,{replace:true})}>
            {route.path}</button>
        ))
      }
      </div>
    </div>
  );
}
export default Navbar;