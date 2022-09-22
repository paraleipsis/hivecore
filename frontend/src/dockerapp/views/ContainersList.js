import React, { Component, useState  } from  'react';
import Modal from 'react-bootstrap/Modal';

import ContainersService  from  '../services/ContainersService';
import Card from 'react-bootstrap/Card';
import start_button from '../../assets/images/start_white.png';
import stop_button from '../../assets/images/stop_white.png';
import pause_button from '../../assets/images/pause_white.png';
import resume_button from '../../assets/images/resume_white.png';
import restart_button from '../../assets/images/restart_white.png';
import terminal_button from '../../assets/images/terminal_white.png';
import remove_button from '../../assets/images/remove_white.png';
import kill_button from '../../assets/images/kill_white.png';

const  containersService  =  new ContainersService();

class  ContainersList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		containers: [],
	};
}

state ={
    openModal : false
}

componentDidMount() {
	var self = this;
	containersService.getContainers().then(function (data) {
		self.setState({containers:  data.result})
	});
}

openNav(info) {
    document.getElementById("mySidenav").style.width = "100%";
};

closeNav() {
    document.getElementById("mySidenav").style.width = "0";
};

container_ports(ports) {
    var size = Object.keys(ports).length;
    var p_ports = ''

    if (size > 0) {
        for (var key in ports) {
            if (ports[key]) {
                for (var host_port in ports[key]) {
                    p_ports += ports[key][host_port]['HostIp'] + ':' + ports[key][host_port]['HostPort'] + '->' + key + ', '
                }
            } else {
                p_ports += key +  ', ';
            }
        }
        return p_ports
    }
    return '-';
}

handleSignal(obj){
	containersService.signalContainer(obj).then((response)=>{
		this.setState({containers:  response.data.result})
	});
}

onClickButton = e =>{
    e.preventDefault()
    this.setState({openModal : true})
}

onCloseModal = ()=>{
    this.setState({openModal : false})
}

ButtonAction (button, containers, container_signal) {
    if (container_signal == 'remove_container') {
        return  <>
                    <button className='button' id={container_signal} onClick={this.onClickButton}>
                        <img src={button} className='action-img'/>
                    </button>

                    <Modal show={this.state.openModal} onHide={this.onCloseModal}>
                        <Modal.Header closeButton>
                        <Modal.Title>Modal heading</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Woohoo, you're reading this text in a modal!</Modal.Body>
                        <Modal.Footer>
                        <button className='button' onClick={this.onCloseModal}>
                            Cancel
                        </button>
                        <button className='button' onClick={() =>{ 
                            this.onCloseModal(); 
                            this.handleSignal({
                                'container_id': containers.items.Id,
                                'container_ip': containers.ip,
                                'container_signal': container_signal
                                });}}>
                            Remove
                        </button>
                        </Modal.Footer>
                    </Modal>
                </>
    } else {
        return <button className='button' id={container_signal}
                onClick={()=>this.handleSignal({
                    'container_id': containers.items.Id,
                    'container_ip': containers.ip,
                    'container_signal': container_signal
                    })}>
            <img src={button} className='action-img'/>
        </button>
    }
}

containerActions(containers) {
    if (containers.items.State.Status == "running") {
        return  <div className='signal-buttons'>
                    {this.ButtonAction(stop_button, containers, 'stop_container')}
                    {this.ButtonAction(restart_button, containers, 'restart_container')}
                    {this.ButtonAction(pause_button, containers, 'pause_container')}
                    {this.ButtonAction(kill_button, containers, 'kill_container')}
                    {this.ButtonAction(terminal_button, containers, 'terminal_container')}
                    {this.ButtonAction(remove_button, containers, 'remove_container')}
                </div>
    } else if (containers.items.State.Status == "paused") {
        return  <div className='signal-buttons'>
                    {this.ButtonAction(resume_button, containers, 'resume_container')}
                    {this.ButtonAction(restart_button, containers, 'restart_container')}
                    {this.ButtonAction(kill_button, containers, 'kill_container')}
                    {this.ButtonAction(terminal_button, containers, 'terminal_container')}
                    {this.ButtonAction(remove_button, containers, 'remove_container')}
                </div>
    } else if (containers.items.State.Status == "exited") {
        return  <div className='signal-buttons'>
                    {this.ButtonAction(start_button, containers, 'start_container')}
                    {this.ButtonAction(restart_button, containers, 'restart_container')}
                    {this.ButtonAction(kill_button, containers, 'kill_container')}
                    {this.ButtonAction(terminal_button, containers, 'terminal_container')}
                    {this.ButtonAction(remove_button, containers, 'remove_container')}
                </div>
    }
}

render() {

    return (
            <section className='containers-section'>

                <div id="main" className="containers--list">

                        {/* main containers table */}
                        <table id="main-table" className="table main-table" cellPadding="0" cellSpacing="0" border="0">
                            <thead key="thead" className='tbl-header main-table-header'>
                                <tr className='main-table-row'>
                                    <th className='images-main-table-tags-header'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Name</th>
                                    <th className='images-main-table-host-header'>Host</th>
                                    <th className='container-status-th'>Status</th>
                                    <th className='container-actions'>Actions</th>
                                    <th className='container-image-th'>Image</th>
                                    <th>IP Address</th>
                                    <th>Ports</th>
                                    <th>Created</th>
                                    
                                </tr>
                            </thead>

                            <tbody className='tbl-content main-table-content'>
                                {this.state.containers.map( c  =>
                                    <tr key={c.items.Id + c.host} className='main-table-row'>
                                    <td>
                                        <button onClick={() => {this.openNav(c)}} className='button'>
                                            {c.items.Name.length > 20 ? c.items.Name.slice(0, 20) + ' ...' : c.items.Name}
                                        </button>
                                    </td>
                                    <td className='images-main-table-host-body'>{c.host}</td>
                                    <td className='container-status-td'>{c.items.State.Status}</td>
                                    <td className='container-actions'>
                                        {this.containerActions(c)}
                                    </td>
                                    <td className='container-image-td'>{c.items.Config.Image.indexOf("@") > -1 ? c.items.Config.Image.slice(0, c.items.Config.Image.indexOf('@')) : c.items.Config.Image}</td>
                                    <td>{Object.values(c.items.NetworkSettings.Networks)[0]['IPAddress'] != '' ? Object.values(c.items.NetworkSettings.Networks)[0]['IPAddress'] : '-'}</td>
                                    <td>{this.container_ports(c.items.NetworkSettings.Ports)}</td>
                                    <td>{c.items.Created.replace('T', ' ').slice(0, c.items.Created.indexOf('.'))}</td>
                                    
                                </tr>)}
                            </tbody>
                        </table>
                </div>
            </section>
	);

  }
}

export  default  ContainersList;