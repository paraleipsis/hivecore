import React, { Component, useState  } from  'react';
import Modal from 'react-bootstrap/Modal';
import ContainersService  from  '../services/ContainersService';
import Card from 'react-bootstrap/Card';
import { Link } from 'react-router-dom';

import start_button from '../../assets/images/start_white.png';
import stop_button from '../../assets/images/stop_white.png';
import pause_button from '../../assets/images/pause_white.png';
import resume_button from '../../assets/images/resume_white.png';
import restart_button from '../../assets/images/restart_white.png';
import terminal_button from '../../assets/images/terminal_white.png';
import remove_button from '../../assets/images/remove_white.png';
import kill_button from '../../assets/images/kill_white.png';
import logs_button from '../../assets/images/logs_white.png';
import stats_button from '../../assets/images/stats_white.png';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

const  containersService  =  new ContainersService();

class  ContainersList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		containers: [],
        containerDetails: [],
        container: '',
        container_ip: '',
        container_signal: '',
        force_remove: false,
        openModal : false
	};
}

componentDidMount() {
	var self = this;
	containersService.getContainers().then(function (data) {
		self.setState({containers:  data.result})
	});
}

detailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({containerDetails: info})
};

closeNavDetails() {
    document.getElementById("details-sidebar").style.width = "0";
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
	containersService.signalContainer(obj)
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

ButtonAction (button, containers, container_signal, signal_name) {
    if (container_signal == 'remove_container') {
        return  <button className='button button-container-signal' id={container_signal} onClick={()=>{this.onClickButtonModal(containers, container_signal); this.handleRefresh}}>
                    <img src={button} className='action-img'/>
                </button>
    } else if (container_signal == 'terminal_container') {
        return <button className='button button-container-signal' id={container_signal}
                onClick={()=>{this.handleSignal({
                    'container': containers.items.Id,
                    'container_ip': containers.ip,
                    'container_signal': container_signal
                    }); window.location.href='/containers/terminal';}}>
            {signal_name}
            <img src={button} className='action-img'/>
        </button>
    } else {
        return <button className='button button-container-signal' id={container_signal}
                onClick={()=>{this.handleSignal({
                    'container': containers.items.Id,
                    'container_ip': containers.ip,
                    'container_signal': container_signal
                    }); this.handleRefresh}}>
            {signal_name}
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


hostStyle(cellContent) {
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

labelsColumns = [
{
    dataField: "labels",
    text: "Labels",
},
];

envColumns = [
{
    dataField: "env",
    text: "Env",
},
];

volumesColumns = [
{
    dataField: "host",
    text: "Path in host",
},
{
    dataField: "container",
    text: "Path in container",
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

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>CONTAINER STATE</Card.Header>
                            <Card.Body className='image-info'>

                                {/* container details table */}
                                {
                                    this.state.containerDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>NAME</th>
                                                <td>{this.state.containerDetails.items.Name}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>STATUS</th>
                                                <td>{this.state.containerDetails.items.State.Status}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>CREATED</th>
                                                <td>{this.state.containerDetails.items.Created.replace('T', ' ').slice(0, this.state.containerDetails.items.Created.indexOf('.'))}</td>

                                                </tr>
                                                {
                                                    this.state.containerDetails.items.State.Status == 'running' ?
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>STARTED AT</th>
                                                    <td>{this.state.containerDetails.items.State.StartedAt.replace('T', ' ').slice(0, this.state.containerDetails.items.State.StartedAt.indexOf('.'))}</td>
                                                    </tr> : 
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>FINISHED AT</th>
                                                    <td>{this.state.containerDetails.items.State.FinishedAt.replace('T', ' ').slice(0, this.state.containerDetails.items.State.FinishedAt.indexOf('.'))}</td>
                                                    </tr>
                                                }
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>ACTIONS</th>
                                                <td>{this.containerActions(this.state.containerDetails)}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }
                                <div className='tools-container-details'>
                                    <table id="table-details" className="table" >
                                        <tbody>
                                            <tr>
                                            <th style={{backgroundColor: 'white'}}>CHECK FOR</th>
                                            <td>
                                                <button id='logs-image' className='button' onClick={this.closeNavDetails}>
                                                    Logs&nbsp;
                                                    <img src={logs_button} className='action-img'/>
                                                </button>
                                                <button id='stats-image' className='button' onClick={this.closeNavDetails}>
                                                    Stats&nbsp;
                                                    <img src={stats_button} className='action-img'/>
                                                </button>
                                            </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>CONTAINER DETAILS</Card.Header>
                            <Card.Body className='image-info'>

                                {/* container details table */}
                                {
                                    this.state.containerDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                            <tr>
                                                <th style={{backgroundColor: 'white'}}>ID</th>
                                                <td>{this.state.containerDetails.items.Id}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>IMAGE</th>
                                                <td>{this.state.containerDetails.items.Config.Image.indexOf("@") > -1 ? 
                                                this.state.containerDetails.items.Config.Image.slice(0, this.state.containerDetails.items.Config.Image.indexOf('@')) : 
                                                this.state.containerDetails.items.Config.Image}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>PORTS</th>
                                                <td>{this.container_ports(this.state.containerDetails.items.NetworkSettings.Ports)}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>CMD</th>
                                                <td>{this.state.containerDetails.items.Config.Cmd == null ?
                                                'No CMD' : this.state.containerDetails.items.Config.Cmd.join(' ')}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>ENTRYPOINT</th>
                                                <td>{this.state.containerDetails.items.Config.Entrypoint == null ?
                                                'No Entrypoint' : this.state.containerDetails.items.Config.Entrypoint.join(', ')}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>WORKDIR</th>
                                                <td>{this.state.containerDetails.items.Config.WorkingDir == '' ?
                                                'No Workdir' : this.state.containerDetails.items.Config.WorkingDir}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }
                                

                                {/* container labels table */}
                                {        
                                    this.state.containerDetails.length != 0 && (
                                        this.state.containerDetails.items.Config.Labels != null &&
                                        Object.keys(this.state.containerDetails.items.Config.Labels).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.containerDetails.items.Config.Labels).map(c => (
                                                {
                                                    labels: c + '=' + this.state.containerDetails.items.Config.Labels[c]
                                                }
                                            ))
                                        }
                                        columns={this.labelsColumns}
                                        /> : 
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            [
                                                {labels: 'No labels'}
                                            ]
                                        }
                                        columns={this.labelsColumns}
                                        />
                                    ) 
                                }

                                {/* container Env table */}
                                {
                                    this.state.containerDetails.length != 0 && (
                                        <BootstrapTable
                                            bootstrap4
                                            keyField="id"
                                            headerClasses = 'tbl-header'
                                            bordered = { false }
                                            data={
                                                Object.keys(this.state.containerDetails.items.Config.Env).map(c => (
                                                    {
                                                        env: this.state.containerDetails.items.Config.Env[c]
                                                    }
                                                ))
                                            }
                                            columns={this.envColumns}
                                        />
                                    )
                                }
                                
                            
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        <Card className='card-info card-dockerfile-details'>

                            <Card.Header className='image-info-header'>VOLUMES</Card.Header>
                            <Card.Body className='image-info'>

                                {/* container volumes table */}
                                {        
                                    this.state.containerDetails.length != 0 && (
                                        this.state.containerDetails.items.Mounts != null &&
                                        this.state.containerDetails.items.Mounts.length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            this.state.containerDetails.items.Mounts.map(c => (
                                                {
                                                    host: c.Source,
                                                    container: c.Destination
                                                }
                                            ))
                                        }
                                        columns={this.volumesColumns}
                                        /> : 
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            [
                                                {host: 'No Volumes'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "host",
                                                text: "Path in host",
                                            }]}
                                        />
                                    ) 
                                }
                                
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        <br/>
                        <br/>

                        <Card className='card-info card-dockerfile-details'>

                            <Card.Header className='image-info-header'>NETWORKS</Card.Header>
                            <Card.Body className='image-info'>

                                <div>connect to network button</div>

                                {/* container networks table */}
                                {        
                                    this.state.containerDetails.length != 0 && (
                                        this.state.containerDetails.items.NetworkSettings.Networks != null &&
                                        this.state.containerDetails.items.NetworkSettings.Networks != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.containerDetails.items.NetworkSettings.Networks).map(c => (
                                                {
                                                    network: c,
                                                    ip: this.state.containerDetails.items.NetworkSettings.Networks[c].IPAddress == '' ?
                                                    '-' : this.state.containerDetails.items.NetworkSettings.Networks[c].IPAddress,
                                                    gateway: this.state.containerDetails.items.NetworkSettings.Networks[c].Gateway == '' ?
                                                    '-' : this.state.containerDetails.items.NetworkSettings.Networks[c].Gateway,
                                                    mac: this.state.containerDetails.items.NetworkSettings.Networks[c].MacAddress == '' ?
                                                    '-' : this.state.containerDetails.items.NetworkSettings.Networks[c].MacAddress,
                                                    actions: 'leave button',
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "network",
                                                text: "NETWORK",
                                            },
                                            {
                                                dataField: "ip",
                                                text: "IP ADDRESS",
                                            },
                                            {
                                                dataField: "gateway",
                                                text: "GATEWAY",
                                            },
                                            {
                                                dataField: "mac",
                                                text: "MAC ADDRESS",
                                            },
                                            {
                                                dataField: "actions",
                                                text: "ACTIONS",
                                            },
                                            ]}
                                        /> : 
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            [
                                                {host: 'No Network'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "networks",
                                                text: "Network",
                                            }]}
                                        />
                                    ) 
                                }
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                    </div>


                        {/* main containers table */}
                    <div>
                        <PaginationProvider
                        pagination={ 
                            paginationFactory({ 
                                sizePerPage: 5, 
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
                                        name: this.detailsSide(c, c.items.Name),
                                        host: this.hostStyle(c.host),
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