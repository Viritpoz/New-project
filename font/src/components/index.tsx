import { RouteObject } from "react-router-dom";
import Map from "./mapPage";
import { SNMP } from "../interfaces/snmp.interface";

// import { SNMP } from "../interfaces/snmp.interface";
// import { useMemo } from "react";


const indexRoutes = (snmpData:SNMP | null,setLoading: React.Dispatch<React.SetStateAction<boolean>>
):RouteObject[] =>[
    {path:"map", element: <Map center={[20.046141, 99.894306]} zoom={15} snmpData={snmpData} setLoading={setLoading}  />, },
    {path: "setting", element: <h1>Setting</h1>, },
]
export default indexRoutes;