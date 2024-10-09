export interface SNMP {
    time: string;
    student: string;
    type: string;
    macAccesspoint: string;
    apName: string;
}


export interface SNMPtotalbuilding{
    total: number;
    floor: SNMPtotalfloor[];
}

export interface SNMPtotalfloor{
    _id:string;
    total: number;
}