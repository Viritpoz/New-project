import Axiosintance, { WS_BASE_URL } from '../../configs/axios.config';
import { useCallback, useEffect, useState } from 'react';
import { SNMP } from '../../interfaces/snmp.interface';

const GetSNMP = () => {
  const [snmpData, setSnmpData] = useState<SNMP[]>([]);
  useEffect(() => {
    async function fetchData() {
      try {
        const response = await Axiosintance.get('/snmp');
        setSnmpData(response.data);
      } catch (error) {
        console.error("Error fetching SNMP data:", error);
      }
    }
    fetchData();
  }, []);
  return snmpData;
}

export const GetSNMPWS = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [snmpData, setSnmpData] = useState<SNMP | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Ensure WS_BASE_URL is correct and doesn't include duplicate '/ws'
  const url = `${WS_BASE_URL}/today`;
 
  useEffect(() => {
    let ws: WebSocket;

    const connectWebSocket = () => {
      ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setSocket(ws);
        setError(null);
      };

      ws.onmessage = (event: MessageEvent) => {
        try {
          const newMessage: SNMP = JSON.parse(event.data);
          setSnmpData(newMessage);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onerror = (error: Event) => {
        console.error('WebSocket error:', error);
        setError('WebSocket connection error');
      };

      ws.onclose = (event: CloseEvent) => {
        console.log('WebSocket disconnected', event.reason);
        setError('WebSocket disconnected');
        
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
      };
    };

    connectWebSocket();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [url]);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const sendMessage = useCallback((message: any) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }, [socket]);

  return { snmpData, sendMessage, error };
};

export default GetSNMP;