import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class NodesService{
	
	constructor(){}
	
	async getNodes() {
		const url = `${API_URL}/dockerapp/nodes/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  
}
