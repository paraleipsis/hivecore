import axios from 'axios';
const API_URL = 'http://localhost:7001';

export default class TerminalService{
	
	constructor(){}
	
	
	async signalTerminal(container) {
		const url = `${API_URL}/dockerapp/containers/`;
		const response = await axios.post(url, container);
        const data = await response.data;
        console.log(data)
	}
	
}
