import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class NetworksService{
	
	constructor(){}
	
	
	async getNetworks() {
		const url = `${API_URL}/dockerapp/networks/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  
	
}
