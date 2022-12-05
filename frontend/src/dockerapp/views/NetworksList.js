import React, { Component } from  'react';
import Modal from 'react-bootstrap/Modal';
import NetworksService  from  '../services/NetworksService';
import Card from 'react-bootstrap/Card';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import remove_button from '../../assets/images/remove_white.png';

const  networksService  =  new NetworksService();

class  NetworksList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		networks: [],
        networkDetails: [],
        openModal : false,
        openModalRemove : false,
        signal: '',
        network: '',
        network_ip: '',
	};
}

componentDidMount() {
	var self = this;
	networksService.getNetworks().then(function (data) {
		self.setState({networks:  data.result})
	});
}

detailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({networkDetails: info})
};

closeNavDetails() {
    document.getElementById("details-sidebar").style.width = "0";
};

handleRefresh = () => {
    this.componentDidMount();
};

hostStyle(cellContent) {
    return <span className='images-main-table-host-body'>{cellContent}</span>
}

action(network) {
    if (network.items.Name != 'host'&& network.items.Name != 'bridge'&& network.items.Name != 'none')
        return <div>
            <button id='remove' onClick={() => {this.onClickButtonModalRemove(network, 'remove_network')}} className='button button-delete'>
                Remove&nbsp;
                <img src={remove_button} className='action-img'/>
            </button>
            </div>
}

onClickButtonModalRemove = (network, signal) => {
    this.setState({
        openModalRemove: true,
        signal: signal,
        network: network.items.Id,
        network_ip: network.ip,
    })
}

onCloseModalRemove = ()=> {
    this.setState({openModalRemove : false})
}

handleRemove(network) {
	networksService.deleteNetwork(network)
}

networksColumnsMain = [
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
    dataField: "driver",
    text: "Driver",
},
{
    dataField: "subnet",
    text: "Subnet"
},
{
    dataField: "gateway",
    text: "Gateway"
},
{
    dataField: "attachable",
    text: "Attachable"
},
{
    dataField: "ipam_driver",
    text: "IPAM Driver"
},
{
    dataField: "actions",
    text: "Actions"
},
];

containersNetwork = [
{
    dataField: "container",
    text: "Container Name",
},
{
    dataField: "ipv4",
    text: "IPv4 Address",
},
{
    dataField: "ipv6",
    text: "IPv6 Address",
},
{
    dataField: "mac",
    text: "MAC Address",
},
{
    dataField: "action",
    text: "Action",
},
];

render() {
    if (this.state.networks == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }

    return (
            <section className='networks-section'>

                <div id="main" className="networks--list">

                    {/* remove network */}
                    <Modal show={this.state.openModalRemove} onHide={this.onCloseModalRemove} dialogClassName="removeConfirm">
                        <Modal.Header closeButton>
                            <Modal.Title>Remove network</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Are you sure you want to remove network: {this.state.network.slice(0, 12)}</Modal.Body>
                        <Modal.Footer>
                                <div className='force_checkbox'>
                                    <input id="force_checkbox" type="checkbox"/>
                                    Force remove
                                </div>
                                <button className='button button-modal-cancel' onClick={this.onCloseModalRemove}>
                                    Cancel
                                </button>
                                <button className='button button-modal-remove' onClick={() =>{ 
                                    this.onCloseModalRemove(); 
                                    this.handleRemove({
                                        'network': this.state.network, 
                                        'network_ip': this.state.network_ip,
                                        'signal': 'remove_network',
                                        'force': document.getElementById('force_checkbox').checked,
                                        })}}>
                                    Remove
                                </button>
                        </Modal.Footer>
                    </Modal>

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>NETWORK DETAILS</Card.Header>
                            <Card.Body className='image-info'>

                                {/* network details table */}
                                {
                                    this.state.networkDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>ID</th>
                                                <td>{this.state.networkDetails.items.Id}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Name</th>
                                                <td>{this.state.networkDetails.items.Name}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Created</th>
                                                <td>{this.state.networkDetails.items.Created.replace('T', ' ').slice(0, this.state.networkDetails.items.Created.indexOf('.'))}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Scope</th>
                                                <td>{this.state.networkDetails.items.Scope}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Driver</th>
                                                <td>{this.state.networkDetails.items.Driver}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Enable IPv6</th>
                                                <td>{this.state.networkDetails.items.EnableIPv6.toString()}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>IPAM Driver</th>
                                                <td>{this.state.networkDetails.items.IPAM.Driver}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Internal</th>
                                                <td>{this.state.networkDetails.items.Internal.toString()}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Attachable</th>
                                                <td>{this.state.networkDetails.items.Attachable.toString()}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Ingress</th>
                                                <td>{this.state.networkDetails.items.Ingress.toString()}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }

                                {/* network config table */}
                                {                         
                                    this.state.networkDetails.length != 0 && (
                                        this.state.networkDetails.items.IPAM.Config != null &&
                                        this.state.networkDetails.items.IPAM.Config.length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            this.state.networkDetails.items.IPAM.Config.map(c => (
                                                {
                                                    subnet: c.Subnet,
                                                    gateway: c.Gateway
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "subnet",
                                                text: "Subnet",
                                            },
                                            {
                                                dataField: "gateway",
                                                text: "Gateway",
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
                                                {config: 'No Network Config'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "config",
                                                text: "Network Config",
                                            },
                                            ]}
                                        />
                                    ) 
                                }

                                {/* network options table */}
                                {                         
                                    this.state.networkDetails.length != 0 && (
                                        this.state.networkDetails.items.Options != null &&
                                        Object.keys(this.state.networkDetails.items.Options).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.networkDetails.items.Options).map(c => (
                                                {
                                                    options: c + '=' + this.state.networkDetails.items.Options[c]
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "options",
                                                text: "Network Options",
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
                                                {options: 'No Network Options'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "options",
                                                text: "Network Options",
                                            },
                                            ]}
                                        />
                                    ) 
                                }

                                {/* network labels table */}
                                {                         
                                    this.state.networkDetails.length != 0 && (
                                        this.state.networkDetails.items.Labels != null &&
                                        Object.keys(this.state.networkDetails.items.Labels).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.networkDetails.items.Labels).map(c => (
                                                {
                                                    labels: c + '=' + this.state.networkDetails.items.Labels[c]
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "labels",
                                                text: "Labels",
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
                                                {labels: 'No Labels'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "labels",
                                                text: "Labels",
                                            },
                                            ]}
                                        />
                                    ) 
                                }
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        <Card className='card-info card-dockerfile-details'>

                            <Card.Header className='image-info-header'>NETWORK CONTAINERS</Card.Header>
                            <Card.Body className='image-info'>

                                {/* network containers table */}
                                {                         
                                    this.state.networkDetails.length != 0 && (
                                        this.state.networkDetails.items.Containers != null &&
                                        Object.keys(this.state.networkDetails.items.Containers).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.networkDetails.items.Containers).map(c => (
                                                {
                                                    container: this.state.networkDetails.items.Containers[c].Name,
                                                    ipv4: this.state.networkDetails.items.Containers[c].IPv4Address,
                                                    ipv6: this.state.networkDetails.items.Containers[c].IPv6Address == '' ?
                                                    '-' : this.state.networkDetails.items.Containers[c].IPv6Address,
                                                    mac: this.state.networkDetails.items.Containers[c].MacAddress,
                                                    actions: 'remove_button',
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "container",
                                                text: "Container ",
                                            },
                                            {
                                                dataField: "ipv4",
                                                text: "IPv4 Address",
                                            },
                                            {
                                                dataField: "ipv6",
                                                text: "IPv6 Address",
                                            },
                                            {
                                                dataField: "mac",
                                                text: "MAC Address",
                                            },
                                            {
                                                dataField: "actions",
                                                text: "Actions",
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
                                                {containers: 'No Containers'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "containers",
                                                text: "Containers",
                                            },
                                            ]}
                                        />
                                    ) 
                                }
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                    </div>


                    {/* main networks table */}
                    <div>
                        <PaginationProvider
                        pagination={ 
                            paginationFactory({ 
                                sizePerPage: 5, 
                                custom: true,
                                totalSize: this.state.networks.length
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
                                data={this.state.networks.map(
                                    c => ({
                                        name: this.detailsSide(c, c.items.Name),
                                        host: this.hostStyle(c.host),
                                        driver: c.items.Driver,
                                        subnet: c.items.IPAM.Config.length != 0 ? c.items.IPAM.Config[0].Subnet : '-',
                                        gateway: c.items.IPAM.Config.length != 0 ? c.items.IPAM.Config[0].Gateway : '-',
                                        attachable: c.items.Attachable,
                                        ipam_driver: c.items.IPAM.Driver,
                                        actions: this.action(c),
                                        }
                                    )
                                )}
                                columns={this.networksColumnsMain}
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
                
                <div className='block'>NETWORK LIST</div>

            </section>
	);

  }
}

export  default  NetworksList;