import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class ContainersService{
	
	constructor(){}
	
	
	async getContainers() {
		const url = `${API_URL}/dockerapp/containers/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  
	
}
