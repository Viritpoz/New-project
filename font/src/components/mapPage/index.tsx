import React, { useEffect, useRef, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { SNMP } from '../../interfaces/snmp.interface';
import { Building, buildingdata } from '../../interfaces/building.interface';
import { getMarkerBuilding } from '../../containers/getMarkerBuilding';
import { GeoJSON } from 'react-leaflet'; 

interface MapProps {
  center: [number, number];
  zoom: number;
  snmpData: SNMP | null;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

const Map: React.FC<MapProps> = ({ center, zoom, snmpData, setLoading }) => {
  const mapRef = useRef<L.Map | null>(null);
  const markersRef = useRef<{ [key: string]: L.Marker }>({});
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const highlightLayerRef = useRef<L.Rectangle<L.LatLngExpression> | null>(null); // Ref to store the highlight rectangle
  const [buildings, setBuildings] = useState<Building | null>(null);
  const [buildingsArea, setBuildingsArea] = useState<Building | null>(null);
  // Ref to store latest props
  const propsRef = useRef({ center, zoom, snmpData });

  

  // Update ref when props change
  useEffect(() => {
    propsRef.current = { center, zoom, snmpData };
  }, [center, zoom, snmpData]);

  // Create map on mount
  useEffect(() => {
    if (!mapContainerRef.current) return;

    mapRef.current = L.map(mapContainerRef.current).setView(center, zoom);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapRef.current);
    const building = getMarkerBuilding();
    setBuildings(building);



    // Cleanup function
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array ensures this runs only on mount/unmount


  // Add markers for buildings
  useEffect(() => {
    if (!mapRef.current || !buildings || Object.keys(buildings).length === 0) return;

    const bounds = L.latLngBounds([]);

    Object.entries(buildings).forEach(([key, building]) => {
      if (!markersRef.current[key]) {
        const marker = L.marker([building.lat, building.lon])
          .addTo(mapRef.current!)
          .bindPopup(building.name)
          .on('click', () => handleMarkerClick(building)); 
          
        markersRef.current[key] = marker;
        // Extend bounds to include each building's coordinates
        bounds.extend([building.lat, building.lon]);
      }
    });

     // Fit map to the bounds of all buildings
     if (bounds.getSouthWest() && bounds.getNorthEast()) {
      mapRef.current.fitBounds(bounds);
    }



    // Cleanup function to remove markers
    return () => {
      Object.values(markersRef.current).forEach(marker => marker.remove());
      markersRef.current = {};
    };
  }, [buildings]);

  // Update map when props change
  useEffect(() => {
    if (!mapRef.current) return;
    // Update center and zoom
    // mapRef.current.setView(propsRef.current.center, propsRef.current.zoom);

    // Update marker based on SNMP data
    if (propsRef.current.snmpData) {
      setLoading(false);
      console.log("Updating map with SNMP data:", propsRef.current.snmpData);

      // Add new marker if SNMP data includes coordinates
      // Adjust this logic based on your SNMP data structure
      // if (propsRef.current.snmpData.latitude && propsRef.current.snmpData.longitude) {
      //   markerRef.current = L.marker([propsRef.current.snmpData.latitude, propsRef.current.snmpData.longitude])
      //     .addTo(mapRef.current)
      //     .bindPopup(`SNMP Data: ${JSON.stringify(propsRef.current.snmpData)}`);
      // }
    }
  }, [center, zoom, snmpData, setLoading]); // This effect runs when any of these props change

  // Handle marker click to fit to building
const handleMarkerClick = (building: buildingdata) => {
  if (highlightLayerRef.current) {
    highlightLayerRef.current.remove();
  }
  const buildname = building.name.split('-')[0];
 
  const node =  buildingArea.elements.find((element) => {
    // console.log(element.tags.name);
    // console.log("Building name: ", buildname.split(' ')[1])    
    if (element.tags.name === buildname.split(' ')[1]) {
      
      return element.nodes;
    }})
  if (!node || node === undefined ) {
    console.log("Node not found");
    return;
  }  

  // Create a small bounding box around the building's location
  const lat = parseFloat(building.lat.toString());
  const lon = parseFloat(building.lon.toString());
  const bounds = L.latLngBounds([
    [lat + 0.0001, lon + 0.0001], // Slightly north-east
    [lat - 0.0001, lon - 0.0001], // Slightly south-west
  ]);

  

  // Fit the map to the bounds
  mapRef.current!.fitBounds(bounds);

  // Optionally add a rectangle to highlight the building's area
  highlightLayerRef.current = L.rectangle(bounds, {
    color: 'blue', // Highlight color
    weight: 2,
  }).addTo(mapRef.current!);
};

  return (
    <div className='h-full p-4'>
      <div ref={mapContainerRef} className='w-full h-full rounded-xl overflow-hidden border-4 border-white' />
    </div>
  );
};

export default Map;