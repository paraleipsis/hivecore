import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class ImagesService{
	
	constructor(){}
	
	
	async getImages() {
		const url = `${API_URL}/dockerapp/images/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  
	
}
