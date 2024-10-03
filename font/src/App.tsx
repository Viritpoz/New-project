
import './App.css'
import './App.sass'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import indexRoutes from '../src/components/index';
import IndexLaouts from './layouts/index.layout';
import { useEffect, useState } from 'react';
import { GetSNMPWS } from './containers/getSNMP';
function App() {
  const { snmpData } = GetSNMPWS();
  const [loading, setLoading] = useState(false);
  const indexroute = indexRoutes(snmpData,setLoading);
  useEffect(()=>{
    if(snmpData !== null){
      setLoading(false);
    }
  },[snmpData,setLoading])
  //  console.log(isConnected);
  return (
    <BrowserRouter>
      <Routes>
          <Route path='/*' element={<IndexLaouts loading={loading} />}>
            {indexroute.map((route, index) => (
              <Route key={index} path={route.path} element={route.element} />
            ))}
          </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
