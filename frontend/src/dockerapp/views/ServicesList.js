import React, { Component } from  'react';
import Modal from 'react-bootstrap/Modal';
import ServicesService  from  '../services/ServicesService';
import Card from 'react-bootstrap/Card';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import remove_button from '../../assets/images/remove_white.png';

const  servicesService  =  new ServicesService();

class  ServicesList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		services: [],
        serviceDetails: [],
        openModal : false,
        openModalRemove : false,
        signal: '',
        service: '',
        service_ip: '',
	};
}

componentDidMount() {
    var self = this;
	servicesService.getServices().then(function (data) {
		self.setState({services:  data.result})
	});
}

detailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({serviceDetails: info})
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

action(service) {
    return <div>
        <button id='remove' onClick={() => {this.onClickButtonModalRemove(service, 'remove_secret')}} className='button button-delete'>
            Remove&nbsp;
            <img src={remove_button} className='action-img'/>
        </button>
        </div>
}

onClickButtonModalRemove = (service, signal) => {
    this.setState({
        openModalRemove: true,
        signal: signal,
        service: service.items.ID,
        service_ip: service.ip,
    })
}

onCloseModalRemove = ()=> {
    this.setState({openModalRemove : false})
}

handleRemove(service) {
	servicesService.deleteServices(service)
}

servicesColumnsMain = [
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
    dataField: "created",
    text: "Created",
},
{
    dataField: "updated",
    text: "Updated",
},
{
    dataField: "actions",
    text: "Actions",
},
];

render() {
    if (this.state.services == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }

    return (
            <section className='services-section'>

                <div id="main" className="services--list">

                    {/* remove service */}
                    <Modal show={this.state.openModalRemove} onHide={this.onCloseModalRemove} dialogClassName="removeConfirm">
                        <Modal.Header closeButton>
                            <Modal.Title>Remove service</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Are you sure you want to remove service: {this.state.service.slice(0, 12)}</Modal.Body>
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
                                        'service': this.state.service, 
                                        'service_ip': this.state.service_ip,
                                        'signal': 'remove_service',
                                        'force': document.getElementById('force_checkbox').checked,
                                        })}}>
                                    Remove
                                </button>
                        </Modal.Footer>
                    </Modal>

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>SERVICE DETAILS</Card.Header>    
                            <Card.Body className='image-info'>
                                {/* service details table */}
                                {
                                    this.state.serviceDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>ID</th>
                                                <td>{this.state.serviceDetails.items.ID}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Name</th>
                                                <td>{this.state.serviceDetails.items.Spec.Name}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Created</th>
                                                <td>{this.state.serviceDetails.items.CreatedAt.replace('T', ' ').slice(0, this.state.serviceDetails.items.CreatedAt.indexOf('.'))}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Updated</th>
                                                <td>{this.state.serviceDetails.items.UpdatedAt.replace('T', ' ').slice(0, this.state.serviceDetails.items.UpdatedAt.indexOf('.'))}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }
                                                            

                                {/* secret labels table */}
                                {                         
                                    this.state.serviceDetails.length != 0 && (
                                        this.state.serviceDetails.items.Spec.Labels != null &&
                                        Object.keys(this.state.serviceDetails.items.Spec.Labels).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.serviceDetails.items.Spec.Labels).map(c => (
                                                {
                                                    labels: c + '=' + this.state.serviceDetails.items.Spec.Labels[c]
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

                    </div>


                    {/* main secrets table */}
                    <div>
                        <PaginationProvider
                        pagination={ 
                            paginationFactory({ 
                                sizePerPage: 5, 
                                custom: true,
                                totalSize: this.state.services.length
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
                                data={this.state.services.map(
                                    c => ({
                                        name: this.detailsSide(c, c.items.Spec.Name),
                                        host: this.hostStyle(c.host),
                                        created: c.items.CreatedAt.replace('T', ' ').slice(0, c.items.CreatedAt.indexOf('.')),
                                        updated: c.items.UpdatedAt.replace('T', ' ').slice(0, c.items.UpdatedAt.indexOf('.')),
                                        actions: this.action(c),
                                        }
                                    )
                                )}
                                columns={this.servicesColumnsMain}
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
                
                <div className='block'>SERVICE LIST</div>

            </section>
	);

  }
}

export  default  ServicesList;