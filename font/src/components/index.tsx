import { RouteObject } from "react-router-dom";
import Map from "./mapPage";
import { SNMP } from "../interfaces/snmp.interface";

// import { SNMP } from "../interfaces/snmp.interface";
// import { useMemo } from "react";


const indexRoutes = (snmpData:SNMP | null,setLoading: React.Dispatch<React.SetStateAction<boolean>>
):RouteObject[] =>[
    {path: "home", element: <h1>Home</h1>, },
    {path:"map", element: <Map center={[20.046141, 99.894306]} zoom={15} snmpData={snmpData} setLoading={setLoading}  />, },
]
export default indexRoutes;