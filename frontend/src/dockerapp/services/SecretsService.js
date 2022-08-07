import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class SecretsService{
	
	constructor(){}
	
	
	async getSecrets() {
		const url = `${API_URL}/dockerapp/secrets/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  
	
}
