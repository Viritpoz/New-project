
import './App.css'
import './App.sass'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import indexRoutes from '../src/components/index';
import IndexLaouts from './layouts/index.layout';
function App() {
  const indexroute = indexRoutes();
  return (
    <BrowserRouter>
      <Routes>
          <Route path='/*' element={<IndexLaouts/>}>
            {indexroute.map((route, index) => (
              <Route key={index} path={route.path} element={route.element} />
            ))}
          </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
