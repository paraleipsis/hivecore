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

	async pullImage(image, tag, node) {
		const url = `${API_URL}/dockerapp/images/`;
		console.log(image, tag, node)
        const response = await axios.post(url, { image: image, tag: tag, node: node });
        const data = await response.data;
		return data;
	}  

	async pruneImages(signal) {
		const url = `${API_URL}/dockerapp/images/`;
		return axios.delete(url, { data: signal });
	}
	
}
