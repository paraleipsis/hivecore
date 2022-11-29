import React, { Component, useEffect, useState  } from  'react';
import ImagesService  from  '../services/ImagesService';
import Card from 'react-bootstrap/Card'
import Modal from 'react-bootstrap/Modal';
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";
import restart_button from '../../assets/images/restart_white.png';
import pull_button from '../../assets/images/pull_image_white.png';
import remove_button from '../../assets/images/remove_white.png';

const  imagesService  =  new  ImagesService();

class  ImagesList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		images: [],
        imageDetails: [],
        signal: '',
	};
}

state = {
    openModal : false
}

imageDetailsSide(object, cellContent) {
    return <button onClick={() => {this.openNavDetails(object)}} className='button'>{cellContent}</button>
}

imageHostStyle(cellContent) {
    return <span className='images-main-table-host-body'>{cellContent}</span>
}

imagesColumnsMain = [
{
    dataField: "repotags",
    text: "Tags",
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
    dataField: "repository",
    text: "Repository",
},
{
    dataField: "used_by",
    text: "Container"
},
{
    dataField: "id",
    text: "ID"
},
{
    dataField: "size",
    text: "Size"
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

componentDidMount() {
	var self = this;
	imagesService.getImages().then(function (data) {
		self.setState({ images:  data.result})
	});
}

handleRefresh = () => {
    this.componentDidMount();
};

openNavDetails(info) {
    document.getElementById("details-sidebar").style.width = "100%";
    this.setState({imageDetails: info})
};

closeNavDetails() {
    document.getElementById("details-sidebar").style.width = "0";
};

openNavPullImage() {
    document.getElementById("pull-sidebar").style.width = "100%";
};

closeNavPullImage() {
    document.getElementById("pull-sidebar").style.width = "0";
};

handleSignal(signal){
	imagesService.pruneImages(signal).then((response)=>{
		this.setState({images:  response.data.result})
	});
}

onClickButtonModal = (signal) =>{
    this.setState({
        openModal: true,
        signal: signal,
    })
}

onCloseModal = ()=>{
    this.setState({openModal : false})
}

render() {

    if (this.state.images == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }
    return (
            
            <section className='images-section'>

                <Modal show={this.state.openModal} onHide={this.onCloseModal} dialogClassName="removeConfirm">
                    <Modal.Header closeButton>
                        <Modal.Title>Prune images</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Are you sure you want to remove unused images on all hosts</Modal.Body>
                    <Modal.Footer>
                            <button className='button button-modal-cancel' onClick={this.onCloseModal}>
                                Cancel
                            </button>
                            <button className='button button-modal-remove' onClick={() =>{ 
                                this.onCloseModal(); 
                                this.handleSignal({
                                    'signal': this.state.signal,
                                    });}}>
                                Remove
                            </button>
                    </Modal.Footer>
                </Modal>

                <div id="pull-sidebar" className="sidenav">
                    <a className="closebtn" onClick={() => {this.closeNavPullImage()}}>&times;</a>
                    <div className='block block-pull'>PULL IMAGE</div>
                </div>

                <div className='tools-title'>IMAGES</div>
                <div className='tools'>
                    <button id='refresh-element' className='button' onClick={this.handleRefresh}>
                        Refresh&nbsp;
                        <img src={restart_button} className='action-img'/>
                    </button>
                    <button id='pull-image' className='button' onClick={this.openNavPullImage}>
                        Pull image&nbsp;
                        <img src={pull_button} className='action-img'/>
                    </button>
                    <button id='prune-images' className='button' onClick={()=>{this.onClickButtonModal('prune_images')}}>
                        Prune images&nbsp;
                        <img src={remove_button} className='action-img'/>
                    </button>
                </div>
            
                <div className="images--list">

                    <div id="details-sidebar" className="sidenav">

                        <a className="closebtn" onClick={() => {this.closeNavDetails()}}>&times;</a>

                            <Card className='card-info card-image-details'>

                                <Card.Header className='image-info-header'>IMAGE DETAILS</Card.Header>
                                <Card.Body className='image-info'>

                                    {/* image details table */}
                                    {
                                        this.state.imageDetails.length != 0 && (
                                            <table id="table-details" className="table" >
                                                <tbody>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>ID</th>
                                                    <td>{this.state.imageDetails.items.Id}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Repository</th>
                                                    <td>{this.state.imageDetails.items.Repository}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Container</th>
                                                    <td>{this.state.imageDetails.items.Used_by}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Tags</th>
                                                    <td>{this.state.imageDetails.items.RepoTags}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Size</th>
                                                    <td>{this.state.imageDetails.items.Size}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Created</th>
                                                    <td>{this.state.imageDetails.items.Created}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Host</th>
                                                    <td>{this.state.imageDetails.host}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Docker Version</th>
                                                    <td>{this.state.imageDetails.items.DockerVersion}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>OS</th>
                                                    <td>{this.state.imageDetails.items.Os}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Architecture</th>
                                                    <td>{this.state.imageDetails.items.Architecture}</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        )
                                    }

                                    
                                    {/* image labels table */}
                                    {        
                                        this.state.imageDetails.length != 0 && (
                                            this.state.imageDetails.items.ContainerConfig.Labels != null &&
                                            Object.keys(this.state.imageDetails.items.ContainerConfig.Labels).length != 0 ?
                                            <BootstrapTable
                                            bootstrap4
                                            keyField="id"
                                            headerClasses = 'tbl-header'
                                            bordered = { false }
                                            data={
                                                Object.keys(this.state.imageDetails.items.ContainerConfig.Labels).map(c => (
                                                    {
                                                        labels: c + '=' + this.state.imageDetails.items.ContainerConfig.Labels[c]
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
                                
                                </Card.Body>

                            </Card>

                            <br/>
                            <br/>

                            <Card className='card-info card-dockerfile-details'>

                                <Card.Header className='image-info-header'>DOCKERFILE</Card.Header>
                                <Card.Body className='image-info'>

                                    {/* image dockerfile table */}
                                    {
                                        this.state.imageDetails.length != 0 && (
                                            <table className="table" >
                                                <tbody>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>CMD</th>
                                                    <td>{this.state.imageDetails.items.Config.Cmd}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>ENTRYPOINT</th>
                                                    <td>{this.state.imageDetails.items.Config.Entrypoint}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Exposed Ports</th>
                                                    <td>{this.state.imageDetails.items.Config.ExposedPorts}</td>
                                                    </tr>
                                                    <tr>
                                                    <th style={{backgroundColor: 'white'}}>Volumes</th>
                                                    <td>{this.state.imageDetails.items.Config.Volumes}</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        )
                                    }

                                    {/* image Env table */}
                                    {
                                        this.state.imageDetails.length != 0 && (
                                            <BootstrapTable
                                                bootstrap4
                                                keyField="id"
                                                headerClasses = 'tbl-header'
                                                bordered = { false }
                                                data={
                                                    Object.keys(this.state.imageDetails.items.Config.Env).map(c => (
                                                        {
                                                            env: this.state.imageDetails.items.Config.Env[c]
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

                            </div>

                    <div>
                            <PaginationProvider
                            pagination={ 
                                paginationFactory({ 
                                    sizePerPage: 5, 
                                    custom: true,
                                    totalSize: this.state.images.length
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
                                    keyField="id"
                                    headerClasses = 'tbl-header'
                                    bordered = { false }
                                    data={this.state.images.map(
                                        c => ({
                                            repotags: this.imageDetailsSide(c, c.items.RepoTags),
                                            host: this.imageHostStyle(c.host),
                                            repository: c.items.Repository,
                                            used_by: c.items.Used_by.slice(0, 12),
                                            id: c.items.Id.slice(c.items.Id.indexOf(':')+1, 19),
                                            size: c.items.Size,
                                            created: c.items.Created
                                            }
                                        )
                                    )}
                                    columns={this.imagesColumnsMain}
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
                
                <div className='block'>IMAGE LIST</div>

            </section>
	);
  }
}

export  default  ImagesList;
