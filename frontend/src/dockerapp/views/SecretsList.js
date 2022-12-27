import React, { Component } from  'react';
import Modal from 'react-bootstrap/Modal';
import SecretsService  from  '../services/SecretsService';
import Card from 'react-bootstrap/Card';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import remove_button from '../../assets/images/remove_white.png';

const  secretsService  =  new SecretsService();

class  SecretsList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		secrets: [],
        secretDetails: [],
        openModal : false,
        openModalRemove : false,
        signal: '',
        secret: '',
        secret_ip: '',
	};
}

componentDidMount() {
    var self = this;
	secretsService.getSecrets().then(function (data) {
		self.setState({secrets:  data.result})
	});
}

detailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({secretDetails: info})
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

action(secret) {
    return <div>
        <button id='remove' onClick={() => {this.onClickButtonModalRemove(secret, 'remove_secret')}} className='button button-delete'>
            Remove&nbsp;
            <img src={remove_button} className='action-img'/>
        </button>
        </div>
}

onClickButtonModalRemove = (secret, signal) => {
    this.setState({
        openModalRemove: true,
        signal: signal,
        secret: secret.items.ID,
        secret_ip: secret.ip,
    })
}

onCloseModalRemove = ()=> {
    this.setState({openModalRemove : false})
}

handleRemove(secret) {
	secretsService.deleteSecret(secret)
}

secretsColumnsMain = [
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
    if (this.state.secrets == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }

    return (
            <section className='secrets-section'>

                <div id="main" className="secrets--list">

                    {/* remove secret */}
                    <Modal show={this.state.openModalRemove} onHide={this.onCloseModalRemove} dialogClassName="removeConfirm">
                        <Modal.Header closeButton>
                            <Modal.Title>Remove secret</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Are you sure you want to remove secret: {this.state.secret.slice(0, 12)}</Modal.Body>
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
                                        'secret': this.state.secret, 
                                        'secret_ip': this.state.secret_ip,
                                        'signal': 'remove_secret',
                                        'force': document.getElementById('force_checkbox').checked,
                                        })}}>
                                    Remove
                                </button>
                        </Modal.Footer>
                    </Modal>

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>SECRET DETAILS</Card.Header>
                            <Card.Body className='image-info'>
                                {/* secret details table */}
                                {
                                    this.state.secretDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>ID</th>
                                                <td>{this.state.secretDetails.items.ID}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Name</th>
                                                <td>{this.state.secretDetails.items.Spec.Name}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Created</th>
                                                <td>{this.state.secretDetails.items.CreatedAt.replace('T', ' ').slice(0, this.state.secretDetails.items.CreatedAt.indexOf('.'))}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Updated</th>
                                                <td>{this.state.secretDetails.items.UpdatedAt.replace('T', ' ').slice(0, this.state.secretDetails.items.UpdatedAt.indexOf('.'))}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }
                                                            

                                {/* secret labels table */}
                                {                         
                                    this.state.secretDetails.length != 0 && (
                                        this.state.secretDetails.items.Spec.Labels != null &&
                                        Object.keys(this.state.secretDetails.items.Spec.Labels).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.secretDetails.items.Spec.Labels).map(c => (
                                                {
                                                    labels: c + '=' + this.state.secretDetails.items.Spec.Labels[c]
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
                                totalSize: this.state.secrets.length
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
                                data={this.state.secrets.map(
                                    c => ({
                                        name: this.detailsSide(c, c.items.Spec.Name),
                                        host: this.hostStyle(c.host),
                                        created: c.items.CreatedAt.replace('T', ' ').slice(0, c.items.CreatedAt.indexOf('.')),
                                        updated: c.items.UpdatedAt.replace('T', ' ').slice(0, c.items.UpdatedAt.indexOf('.')),
                                        actions: this.action(c),
                                        }
                                    )
                                )}
                                columns={this.secretsColumnsMain}
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
                
                <div className='block'>SECRET LIST</div>

            </section>
	);

  }
}

export  default  SecretsList;