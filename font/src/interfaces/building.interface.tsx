export interface Building {
    [key: string]: buildingdata
}

export interface buildingdata{
    "name": string,
    lat: number,
    lon: number,
    aps: string[]
}
