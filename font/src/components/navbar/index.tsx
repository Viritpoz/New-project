import React from 'react';
import { useNavigate } from "react-router-dom";
import indexRoutes from '../index';
const Navbar: React.FC = () => {
 const indexRoute = indexRoutes();
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