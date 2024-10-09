import Axiosintance, { WS_BASE_URL } from '../../configs/axios.config';
import  { useCallback, useEffect, useRef, useState } from 'react';
import { SNMP, SNMPtotalbuilding } from '../../interfaces/snmp.interface';

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

// export const testGetSNMPWSBuilding = (building: string): Promise<void> =>{
//   const useWebSocket = (baseUrl: string) => {
//     const socketRef = useRef<WebSocket | null>(null);
//     const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  
//     const closeSocket = useCallback(() => {
//       if (socketRef.current) {
//         console.log("Closing WebSocket connection");
//         socketRef.current.close();
//         socketRef.current = null;
//       }
//       if (reconnectTimeoutRef.current) {
//         clearTimeout(reconnectTimeoutRef.current);
//         reconnectTimeoutRef.current = null;
//       }
//     }, []);
  
//     const connectWebSocket = useCallback((building: string) => {
//       closeSocket(); // Always close the existing connection first
  
//       return new Promise<void>((resolve, reject) => {
//         const url = `${baseUrl}/today/total/${building}`;
//         console.log(`Connecting to WebSocket: ${url}`);
        
//         const socket = new WebSocket(url);
//         socketRef.current = socket;
  
//         socket.onopen = () => {
//           console.log(`WebSocket connected for building: ${building}`);
//           resolve();
//         };
  
//         socket.onmessage = (event) => {
//           const data = JSON.parse(event.data);
//           console.log("Received data: ", data);
//           // Handle the received data here
//         };
  
//         socket.onclose = (event) => {
//           console.log(`WebSocket disconnected for building: ${building}`, event.reason);
//           socketRef.current = null;
//           // Optionally implement reconnection logic here
//         };
  
//         socket.onerror = (error) => {
//           console.error("WebSocket error: ", error);
//           reject(error);
//         };
//       });
//     }, [closeSocket]);
  
//     useEffect(() => {
//       return () => {
//         closeSocket(); // Ensure socket is closed when component unmounts
//       };
//     }, [closeSocket]);
  
//     return { connectWebSocket, closeSocket };
//   };
  
// };


export const GetSNMPWSBuilding = () => {
  const socketRef = useRef<WebSocket | null>(null);
  const [snmptotalData, setSnmptotalData] = useState<SNMPtotalbuilding | null>(null);
  const [selectedBuilding, setSelectedBuilding] = useState<string | null>(null);

  const closeSocket = useCallback(() => {
    if (socketRef.current) {
      console.log("Closing WebSocket connection");
      socketRef.current.close();
      socketRef.current = null;
    }
  }, []);

  const connectWebSocket = useCallback((building: string) => {
    closeSocket(); // Always close the existing connection first

    return new Promise<void>((resolve, reject) => {
      const url = `${WS_BASE_URL}/today/total/${building}`;
      console.log(`Connecting to WebSocket: ${url}`);
      
      const socket = new WebSocket(url);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log(`WebSocket connected for building: ${building}`);
        setSelectedBuilding(building);
        resolve();
      };

      socket.onmessage = (event) => {
        try {
          const newData: SNMPtotalbuilding = JSON.parse(event.data);
          setSnmptotalData(newData);
          // console.log("Received data: ", newData);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      socket.onclose = (event) => {
        console.log(`WebSocket disconnected for building: ${building}`, event.reason);
        socketRef.current = null;
        // Optionally implement reconnection logic here
      };

      socket.onerror = (error) => {
        console.error("WebSocket error: ", error);
        reject(error);
      };
    });
  }, [closeSocket]);

  useEffect(() => {
    return () => {
      closeSocket(); // Ensure socket is closed when component unmounts
    };
  }, [closeSocket]);

  return { connectWebSocket, closeSocket, snmptotalData, selectedBuilding };
};
export default GetSNMP;