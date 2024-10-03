import { Building } from "../../interfaces/building.interface";

const buildings : Building = {
    "M SQUARE": { "name": "Building M SQUARE", "lat": 20.046071935691224,  "lon": 99.890827797351, "aps": ["AP1", "AP2"] },
    "S1": { "name": "Building S1", "lat": 20.045715467409458,  "lon": 99.89441733931345, "aps": ["AP1", "AP2"] },
    "S2": { "name": "Building S2", "lat": 20.04556932361864, "lon": 99.89587914323758, "aps": ["AP3", "AP4"] },
    "S3": { "name": "Building S3", "lat": 20.045864130773094, "lon": 99.89544730757953, "aps": ["AP3", "AP4"] },
    "S4": { "name": "Building S4", "lat": 20.04618161477225, "lon": 99.89509057377654, "aps": ["AP3", "AP4"] },
    "S5": { "name": "Building S5", "lat": 20.046672957812408, "lon": 99.89513617132967, "aps": ["AP3", "AP4"] },
    "S6": { "name": "Building S6", "lat": 20.047008078066487, "lon": 99.89480894182617, "aps": ["AP3", "AP4"] },
    "S7": { "name": "Building S7", "lat": 20.047595166725053, "lon": 99.89572625731729, "aps": ["AP3", "AP4"] },
    "C1": { "name": "Building C1", "lat": 20.04500238523902, "lon": 99.89544998978366, "aps": ["AP3", "AP4"] },
    "C2": { "name": "Building C2", "lat": 20.044246464211735, "lon": 99.89599984263437, "aps": ["AP3", "AP4"] },
    "C3": { "name": "Building C3", "lat": 20.044027246432005, "lon": 99.89500474308677, "aps": ["AP3", "AP4"] },
    "C4": { "name": "Building C4", "lat": 20.04407260186479, "lon": 99.89449244116557, "aps": ["AP3", "AP4"] },
    "C5": { "name": "Building C5", "lat": 20.04294879129814, "lon": 99.89497792100154, "aps": ["AP3", "AP4"] },
    "AD": { "name": "Building AD", "lat": 20.04500357351408, "lon": 99.89667501300173, "aps": ["AP3", "AP4"] },
    "E1": { "name": "Building E1", "lat": 20.045626017347796, "lon": 99.8935670790481, "aps": ["AP3", "AP4"] },
    "E2": { "name": "Building E2", "lat": 20.04437182136767, "lon": 99.89354428027745, "aps": ["AP3", "AP4"] },
    "E3": { "name": "Building E3", "lat": 20.0460997241167, "lon": 99.8926403758338, "aps": ["AP3", "AP4"] },
    "E4": { "name": "Building E4", "lat": 20.04432292979196, "lon": 99.89029202611252, "aps": ["AP3", "AP4"] },
    "AS": { "name": "Building AS", "lat": 20.046172409238665, "lon": 99.89362869411906, "aps": ["AP3", "AP4"] },
    "AV": { "name": "Building AV", "lat": 20.046671311398228, "lon": 99.89343557506781, "aps": ["AP3", "AP4"] },
    "D1": { "name": "Building D1", "lat": 20.047326433053613, "lon": 99.89370379596953, "aps": ["AP3", "AP4"] },
    "D2": { "name": "Building D2", "lat": 20.05180669898016,  "lon": 99.89305939525963, "aps": ["AP3", "AP4"] },
    "F1": { "name": "Building F1", "lat": 20.04830911040164, "lon": 99.8944548144965, "aps": ["AP3", "AP4"] },
    "F2": { "name": "Building F2", "lat": 20.04836958265219, "lon": 99.89399347454075, "aps": ["AP3", "AP4"] },
    "F3": { "name": "Building F3", "lat": 20.049881381369, "lon": 99.89386472850629, "aps": ["AP3", "AP4"] },
    "F4": { "name": "Building F4", "lat": 20.048606432099074, "lon": 99.89264700559983, "aps": ["AP3", "AP4"] },
    "F5": { "name": "Building F5", "lat": 20.049926735126895, "lon": 99.89193890242058, "aps": ["AP3", "AP4"] },
    "F6": { "name": "Building F6", "lat": 20.050330193831037, "lon": 99.89206161348778, "aps": ["AP3", "AP4"] },
    "Sak1": { "name": "Building Sak1", "lat": 20.049836342603957, "lon": 99.89286627620132, "aps": ["AP3", "AP4"] },
    "Sak2": { "name": "Building Sak2", "lat": 20.050155078395125, "lon": 99.89298697560832, "aps": ["AP3", "AP4"] },
    "Sak3": { "name": "Building Sak3", "lat": 20.050676644666325, "lon": 99.8931157216486, "aps": ["AP3", "AP4"] },
    "Pao": { "name": "Building Pao", "lat": 20.05063381079076, "lon": 99.89245858043058, "aps": ["AP3", "AP4"] },
    "PS": { "name": "Building PS", "lat": 20.050875696078602, "lon": 99.89202138036042, "aps": ["AP3", "AP4"] },
    "BS": { "name": "Building BS", "lat": 20.05142245622511, "lon": 99.8920079693152, "aps": ["AP3", "AP4"] },
    "A1": { "name": "Building A1", "lat": 20.05298083821384,  "lon": 99.89558603616301, "aps": ["AP3", "AP4"] },
    "A2": { "name": "Building A2", "lat": 20.054089459447102, "lon": 99.89514078946154, "aps": ["AP3", "AP4"] },
    "Pool": { "name": "Building Pool", "lat": 20.055666711651387,  "lon": 99.8949852213377, "aps": ["AP3", "AP4"] },
    
    
    // ... Add all 60 buildings
};

export const getMarkerBuilding = () => {
    return buildings;
}
