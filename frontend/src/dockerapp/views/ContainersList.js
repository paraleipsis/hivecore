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

// paginate table
import BootstrapTable from "react-bootstrap-table-next";
// import paginationFactory from "react-bootstrap-table2-paginator";
import paginationFactory, { PaginationProvider, PaginationListStandalone, SizePerPageDropdownStandalone  } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
// import 'react-bootstrap-table2-paginator/dist/react-bootstrap-table2-paginator.min.css';
// 

const  containersService  =  new ContainersService();

class  ContainersList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		containers: [],
        container: '',
        container_ip: '',
        container_signal: '',
        force_remove: false,
	};
}

state = {
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

onClickButtonModal = (containers, container_signal) =>{
    this.setState({
        openModal: true,
        container: containers.items.Id,
        container_ip: containers.ip,
        container_signal: container_signal,
    })
}

onCloseModal = ()=>{
    this.setState({openModal : false})
}

handleRefresh = () => {
    this.componentDidMount();
};

ButtonAction (button, containers, container_signal) {
    if (container_signal == 'remove_container') {
        return  <button className='button' id={container_signal} onClick={()=>{this.onClickButtonModal(containers, container_signal); this.handleRefresh}}>
                    <img src={button} className='action-img'/>
                </button>
    } else {
        return <button className='button' id={container_signal}
                onClick={()=>{this.handleSignal({
                    'container': containers.items.Id,
                    'container_ip': containers.ip,
                    'container_signal': container_signal
                    }); this.handleRefresh}}>
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
                    {this.ButtonAction(remove_button, containers, 'remove_container')}
                </div>
    } else if (containers.items.State.Status == "exited") {
        return  <div className='signal-buttons'>
                    {this.ButtonAction(start_button, containers, 'start_container')}
                    {this.ButtonAction(restart_button, containers, 'restart_container')}
                    {this.ButtonAction(kill_button, containers, 'kill_container')}
                    {this.ButtonAction(remove_button, containers, 'remove_container')}
                </div>
    }
}

containerDetailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNav(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

containerHostStyle(cellContent) {
    return <span className='images-main-table-host-body'>{cellContent}</span>
}

containersColumnsMain = [
{
    dataField: "name",
    text: "Name",
    sort: true,
    headerClasses: 'images-main-table-tags-header',
    editCellClasses: 'images-main-table-repotags-body'
},
{
    dataField: "host",
    text: "Host",
    sort: true,
    headerClasses: 'images-main-table-host-header',
},
{
    dataField: "status",
    text: "Status",
},
{
    dataField: "actions",
    text: "Actions"
},
{
    dataField: "image",
    text: "Image"
},
{
    dataField: "ip_address",
    text: "IP Address"
},
{
    dataField: "ports",
    text: "Ports"
},
{
    dataField: "created",
    text: "Created"
},
];

render() {
    if (this.state.containers == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }

    return (
            <section className='containers-section'>

                <Modal show={this.state.openModal} onHide={this.onCloseModal} dialogClassName="removeConfirm">
                    <Modal.Header closeButton>
                        <Modal.Title>Remove container</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Are you sure you want to remove container: {this.state.container.slice(0, 12)}</Modal.Body>
                    <Modal.Footer>
                            <div className='force_checkbox'>
                                <input id="force_checkbox" type="checkbox"/>
                                Force remove
                            </div>
                            <div className='volumes_checkbox'>
                                <input id="volumes_checkbox" type="checkbox"/>
                                Remove the volumes associated with the container
                            </div>
                            <button className='button button-modal-cancel' onClick={this.onCloseModal}>
                                Cancel
                            </button>
                            <button className='button button-modal-remove' onClick={() =>{ 
                                this.onCloseModal(); 
                                this.handleSignal({
                                    'container': this.state.container,
                                    'container_ip': this.state.container_ip,
                                    'container_signal': this.state.container_signal,
                                    'force': document.getElementById('force_checkbox').checked,
                                    'v': document.getElementById('volumes_checkbox').checked,
                                    });}}>
                                Remove
                            </button>
                    </Modal.Footer>
                </Modal>

                <div id="main" className="containers--list">

                        {/* main containers table */}
                        <div>
                        <PaginationProvider
                        pagination={ 
                            paginationFactory({ 
                                sizePerPage: 3, 
                                custom: true,
                                totalSize: this.state.containers.length
                            })}
                        >
                        {
                            ({
                            paginationProps,
                            paginationTableProps
                            }) => (
                            <div>

                                <BootstrapTable
                                bootstrap4
                                keyField="name"
                                headerClasses = 'tbl-header'
                                bordered = { false }
                                data={this.state.containers.map(
                                    c => ({
                                        name: this.containerDetailsSide(c, c.items.Name),
                                        host: this.containerHostStyle(c.host),
                                        status: c.items.State.Status,
                                        actions: this.containerActions(c),
                                        image: c.items.Config.Image.indexOf("@") > -1 ? c.items.Config.Image.slice(0, c.items.Config.Image.indexOf('@')) : c.items.Config.Image,
                                        ip_address: Object.values(c.items.NetworkSettings.Networks)[0]['IPAddress'] != '' ? Object.values(c.items.NetworkSettings.Networks)[0]['IPAddress'] : '-',
                                        ports: this.container_ports(c.items.NetworkSettings.Ports),
                                        created: c.items.Created.replace('T', ' ').slice(0, c.items.Created.indexOf('.')),
                                        }
                                    )
                                )}
                                columns={this.containersColumnsMain}
                                { ...paginationTableProps }
                                />

                                <PaginationListStandalone
                                    {...paginationProps}
                                />

                            </div>
                            )
                        }
                        </PaginationProvider>
                    </div>

                </div>
                
                <div className='block'>CONTAINER LIST</div>

            </section>
	);

  }
}

export  default  ContainersList;