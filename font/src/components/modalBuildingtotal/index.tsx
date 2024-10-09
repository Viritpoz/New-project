import { useEffect } from "react";
import { modalBuildingtotal } from "../../interfaces/modalBuildingtotal.interface";

const ModalBuildingtotal: React.FC<modalBuildingtotal> = ({ 
    building,
    selectedBuilding,
    setModalBuildingtotalVisible,
    modalBuildingtotalVisible,
    closeWebSocket 
  }) => {
    useEffect(() => {
      console.log("Modal visibility changed:", modalBuildingtotalVisible);
      console.log("Building data:", building);
      if (!modalBuildingtotalVisible) {
        closeWebSocket();
      }
    }, [modalBuildingtotalVisible, building, closeWebSocket]);
  
    if (!building) {
      console.log("No building data available");
      return null;
    }
    console.log(building);
    return (
        <div
        className={`fixed inset-0 z-50 flex items-center justify-end transition-opacity bg-black bg-opacity-50 duration-300 ${
          modalBuildingtotalVisible ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        style={{ zIndex: 1000 }}  // Ensure the modal stays above the map
      >
        <div
          className={`bg-red-800 rounded-lg p-4 w-fit max-w-md transform transition-transform duration-300 ease-in-out ${
            modalBuildingtotalVisible ? 'translate-x-0' : 'translate-x-full'
          }`}
          style={{ marginRight: '20px' }}  // Adjusts the right margin
        >
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-bold">Building {selectedBuilding}</h2>
            <button
              onClick={() => setModalBuildingtotalVisible(false)}
              className="text-white hover:text-gray-700"
            >
              ×
            </button>
          </div>
          <div className="max-h-96 overflow-auto">
            {building.floor.map((floor, index) => (
              <div key={index} className="mb-2 p-2 px-10 bg-white rounded text-red-800">
                <h3 className="font-semibold">{floor._id}</h3>
                <p>Total: {floor.total}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
      
    );
  };
  
  export default ModalBuildingtotal;