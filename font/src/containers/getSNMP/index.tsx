import Axiosintance, { WS_BASE_URL } from '../../configs/axios.config';
import { useCallback, useEffect, useRef, useState } from 'react';
import { SNMP } from '../../interfaces/snmp.interface';

const GetSNMP = () => {
    const [snmpData, setSnmpData] = useState([]);
    useEffect(() => {
        async function fetchData() {
            const response = await Axiosintance.get('/snmp');
            setSnmpData(response.data);
        }
        fetchData();
    }, []);
    return snmpData;

}

export const GetSNMPWS = () => {
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [snmpData, setSnmpData] = useState<SNMP | null>(null);
    const [isConnected, setIsConnected] = useState(false);
    const reconnectTimeoutRef = useRef<number>();
  
    const connect = useCallback(() => {
      const ws = new WebSocket(`${WS_BASE_URL}/today`);
  
      ws.onopen = () => {
        console.log("Connected to WebSocket");
        setSocket(ws);
        setIsConnected(true);
      };
  
      ws.onmessage = (message: MessageEvent) => {
        try {
          const data = JSON.parse(message.data);
          setSnmpData(data);
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };
  
      ws.onclose = (event) => {
        console.log("WebSocket disconnected:", event.reason);
        setIsConnected(false);
        reconnectTimeoutRef.current = window.setTimeout(connect, 5000);
      };
  
      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
  
      return ws;
    }, []);
  
    useEffect(() => {
      const ws = connect();
  
      return () => {
        clearTimeout(reconnectTimeoutRef.current);
        if (ws) {
          ws.close();
        }
      };
    }, [connect]);
  
    const send = useCallback((message: string) => {
      if (socket && isConnected) {
        socket.send(message);
      } else {
        console.warn("WebSocket is not connected. Message not sent.");
      }
    }, [socket, isConnected]);
  
    return { snmpData, send, isConnected };
  };


export default GetSNMP;