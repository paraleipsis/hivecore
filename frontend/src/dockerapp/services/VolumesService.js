import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class VolumesService{
	
	constructor(){}
	
	
	async getVolumes() {
		const url = `${API_URL}/dockerapp/volumes/`;
        const response = await axios.get(url);
        const data = await response.data;
		return data;
	}  

	async deleteVolume(volume) {
		const url = `${API_URL}/dockerapp/volumes/`;
		console.log(volume)
		// return axios.delete(url, { data: volume });
	}
	
}
