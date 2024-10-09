
import './App.css'
import './App.sass'
import { BrowserRouter, Routes, Route, Navigate  } from "react-router-dom";
import indexRoutes from '../src/components/index';
import IndexLaouts from './layouts/index.layout';
import { useEffect, useState } from 'react';
import { GetSNMPWS } from './containers/getSNMP';
function App() {
  const { snmpData } = GetSNMPWS();
  const [loading, setLoading] = useState(false);
  const indexroute = indexRoutes(snmpData,setLoading);
  // const navigate = useNavigate();
  useEffect(()=>{
    if(snmpData !== null){
      setLoading(false);
    }
  },[snmpData,setLoading])

  // useEffect(() => {
  //   if (window.location.pathname === "/") {
  //     navigate("/map"); // Redirect to "/map" if the path is empty
  //   }
  // }, [navigate]);

  //  console.log(isConnected);
  return (
    <BrowserRouter>
    
      <Routes>
      <Route
          path="/"
          element={<Navigate to="/map" replace />}
        />

          <Route path='/*' element={<IndexLaouts snmpData={snmpData} setLoading={setLoading} loading={loading} />}>
            {indexroute.map((route, index) => (
              <Route key={index} path={route.path} element={route.element} />
            ))}
          </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
