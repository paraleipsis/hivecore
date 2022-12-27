import React, { Component } from  'react';
import Modal from 'react-bootstrap/Modal';
import VolumesService  from  '../services/VolumesService';
import Card from 'react-bootstrap/Card';

import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import remove_button from '../../assets/images/remove_white.png';

const  volumesService  =  new VolumesService();

class  VolumesList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		volumes: [],
        volumeDetails: [],
        openModal : false,
        openModalRemove : false,
        signal: '',
        volume: '',
        volume_ip: '',
	};
}

componentDidMount() {
    var self = this;
	volumesService.getVolumes().then(function (data) {
		self.setState({volumes:  data.result})
	});
}

detailsSide(object, cellContentName) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContentName.length > 20 ? cellContentName.slice(0, 20) + ' ...' : cellContentName}</button>
}

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({volumeDetails: info})
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

action(volume) {
    return <div>
        <button id='remove' onClick={() => {this.onClickButtonModalRemove(volume, 'remove_volume')}} className='button button-delete'>
            Remove&nbsp;
            <img src={remove_button} className='action-img'/>
        </button>
        </div>
}

onClickButtonModalRemove = (volume, signal) => {
    this.setState({
        openModalRemove: true,
        signal: signal,
        volume: volume.items.Name,
        volume_ip: volume.ip,
    })
}

onCloseModalRemove = ()=> {
    this.setState({openModalRemove : false})
}

handleRemove(volume) {
	volumesService.deleteVolume(volume)
}

volumesColumnsMain = [
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
    dataField: "scope",
    text: "Scope"
},
{
    dataField: "containers",
    text: "Containers"
},
{
    dataField: "created",
    text: "Created"
},
{
    dataField: "actions",
    text: "Actions"
},
];

render() {
    if (this.state.volumes == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }

    return (
            <section className='volumes-section'>

                <div id="main" className="volumes--list">

                    {/* remove volume */}
                    <Modal show={this.state.openModalRemove} onHide={this.onCloseModalRemove} dialogClassName="removeConfirm">
                        <Modal.Header closeButton>
                            <Modal.Title>Remove volume</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Are you sure you want to remove volume: {this.state.volume.slice(0, 12)}</Modal.Body>
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
                                        'volume': this.state.volume, 
                                        'volume_ip': this.state.volume_ip,
                                        'signal': 'remove_volume',
                                        'force': document.getElementById('force_checkbox').checked,
                                        })}}>
                                    Remove
                                </button>
                        </Modal.Footer>
                    </Modal>

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>VOLUME DETAILS</Card.Header>
                            <Card.Body className='image-info'>

                                {/* volume details table */}
                                {
                                    this.state.volumeDetails.length != 0 && (
                                        <table id="table-details" className="table" >
                                            <tbody>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Name</th>
                                                <td>{this.state.volumeDetails.items.Name}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Created</th>
                                                <td>{this.state.volumeDetails.items.CreatedAt.replace('T', ' ').slice(0, this.state.volumeDetails.items.CreatedAt.indexOf('+'))}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Mountpoint</th>
                                                <td>{this.state.volumeDetails.items.Mountpoint}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Driver</th>
                                                <td>{this.state.volumeDetails.items.Driver}</td>
                                                </tr>
                                                <tr>
                                                <th style={{backgroundColor: 'white'}}>Scope</th>
                                                <td>{this.state.volumeDetails.items.Scope}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    )
                                }
                                

                                {/* volume options table */}
                                {                         
                                    this.state.volumeDetails.length != 0 && (
                                        this.state.volumeDetails.items.Options != null &&
                                        Object.keys(this.state.volumeDetails.items.Options).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.volumeDetails.items.Options).map(c => (
                                                {
                                                    options: c + '=' + this.state.volumeDetails.items.Options[c]
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "options",
                                                text: "Volume Options",
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
                                                {options: 'No Volume Options'}
                                            ]
                                        }
                                        columns={[
                                            {
                                                dataField: "options",
                                                text: "Volume Options",
                                            },
                                            ]}
                                        />
                                    ) 
                                }
                                

                                {/* volume labels table */}
                                {                         
                                    this.state.volumeDetails.length != 0 && (
                                        this.state.volumeDetails.items.Labels != null &&
                                        Object.keys(this.state.volumeDetails.items.Labels).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.volumeDetails.items.Labels).map(c => (
                                                {
                                                    labels: c + '=' + this.state.volumeDetails.items.Labels[c]
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

                            <Card.Header className='image-info-header'>VOLUME CONTAINERS</Card.Header>
                            <Card.Body className='image-info'>

                                {/* volume containers table */}
                                {                         
                                    this.state.volumeDetails.length != 0 && (
                                        this.state.volumeDetails.items.Containers != null &&
                                        Object.keys(this.state.volumeDetails.items.Containers).length != 0 ?
                                        <BootstrapTable
                                        bootstrap4
                                        keyField="id"
                                        headerClasses = 'tbl-header'
                                        bordered = { false }
                                        data={
                                            Object.keys(this.state.volumeDetails.items.Containers).map(c => (
                                                {
                                                    container: this.state.volumeDetails.items.Containers[c].container_name.length > 20 ? 
                                                    this.state.volumeDetails.items.Containers[c].container_name.slice(0, 20) + ' ...' : 
                                                    this.state.volumeDetails.items.Containers[c].container_name,
                                                    mounted: this.state.volumeDetails.items.Containers[c].destination,
                                                    read_only: !this.state.volumeDetails.items.Containers[c].container_rw,
                                                    
                                                }
                                            ))
                                        }
                                        columns={[
                                            {
                                                dataField: "container",
                                                text: "Container ",
                                            },
                                            {
                                                dataField: "mounted",
                                                text: "Mounted At",
                                            },
                                            {
                                                dataField: "read_only",
                                                text: "Read-only",
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


                    {/* main volume table */}
                    <div>
                        <PaginationProvider
                        pagination={ 
                            paginationFactory({ 
                                sizePerPage: 5, 
                                custom: true,
                                totalSize: this.state.volumes.length
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
                                data={this.state.volumes.map(
                                    c => ({
                                        name: this.detailsSide(c, c.items.Name),
                                        host: this.hostStyle(c.host),
                                        driver: c.items.Driver,
                                        scope: c.items.Scope,
                                        containers: c.items.Containers ?
                                        'Used' : 'Unused',
                                        created: c.items.CreatedAt.replace('T', ' ').slice(0, c.items.CreatedAt.indexOf('+')),
                                        actions: this.action(c),
                                        }
                                    )
                                )}
                                columns={this.volumesColumnsMain}
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
                
                <div className='block'>VOLUME LIST</div>

            </section>
	);

  }
}

export  default  VolumesList;