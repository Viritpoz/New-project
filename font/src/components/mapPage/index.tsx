import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { GetSNMPWS } from '../../containers/getSNMP/index';
interface MapProps {
  center: [number, number];
  zoom: number;
}

const Map: React.FC<MapProps> = ({ center = [13.7563, 100.5018], zoom = 13 }) => {
  const mapRef = useRef<L.Map | null>(null);

  const { snmpData, send, isConnected } = GetSNMPWS();
 
  useEffect(() => {
    
    if (!mapRef.current) {
      mapRef.current = L.map('map', {
        center: center,
        zoom: zoom,
        layers: [
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }),
        ],
      });
    }
    
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, [center, zoom]);

  useEffect(() => {
    if (snmpData) {
      console.log("Received SNMP data:", snmpData);
    }
  }, [snmpData]);
  return (
    <div className='h-full p-4'>
        <div id="map" className=' w-full h-full rounded-xl overflow-hidden border-4 border-white ' />
    </div>
    
    );

    };

export default Map;