import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class ConfigsService{
	
	constructor(){}
	
	
	async getConfigs() {
		const url = `${API_URL}/dockerapp/configs/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  
	
}
