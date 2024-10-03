export const fetchBuildings = async () => {
    const response = await fetch('https://overpass-api.de/api/interpreter?data=[out:json];(way["building"](20.04271,99.88860,20.05908,99.90297);relation["building"](20.04271,99.88860,20.05908,99.90297););out body;>;out skel qt;');
    const data = await response.json();
    return data;
  };