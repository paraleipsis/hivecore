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

	async pullImage(image, tag, node, signal) {
		const url = `${API_URL}/dockerapp/images/`;
        return axios.post(url, { image: image, tag: tag, node: node, signal: signal });
	}  

	async pruneImages(signal) {
		const url = `${API_URL}/dockerapp/images/`;
		return axios.delete(url, { data: signal });
	}

	async deleteImage(image) {
		const url = `${API_URL}/dockerapp/images/`;
		return axios.delete(url, { data: image });
	}

	async tagImage(image, tag, repository, node, signal) {
		const url = `${API_URL}/dockerapp/images/`;
		return axios.post(url, { image: image, repository: repository, tag: tag, node: node, signal: signal });
	}
	
}
