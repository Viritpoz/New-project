import { SNMPtotalbuilding } from "./snmp.interface";

export interface modalBuildingtotal {
    building:SNMPtotalbuilding | null;
    selectedBuilding:string | null;
    setModalBuildingtotalVisible:React.Dispatch<React.SetStateAction<boolean>>;
    modalBuildingtotalVisible:boolean;
    closeWebSocket:()=>void;
}