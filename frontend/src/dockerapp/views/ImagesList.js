import React, { Component } from  'react';

import ImagesService  from  '../services/ImagesService';
import NodesService  from  '../services/NodesService';

import Card from 'react-bootstrap/Card'
import Modal from 'react-bootstrap/Modal';
import Select from 'react-select'
import BootstrapTable from "react-bootstrap-table-next";
import paginationFactory, { PaginationProvider, PaginationListStandalone } from 'react-bootstrap-table2-paginator';
import "react-bootstrap-table-next/dist/react-bootstrap-table2.min.css";

import $ from 'jquery';

import restart_button from '../../assets/images/restart_white.png';
import pull_button from '../../assets/images/pull_image_white.png';
import remove_button from '../../assets/images/remove_white.png';
import tag_button from '../../assets/images/tag_image_white.png';

const  imagesService = new ImagesService();
const  nodesService = new NodesService();

class  ImagesList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		images: [],
        imageDetails: [],
        nodes: [],
        signal: '',
        inputImage: '',
        inputImageError: 'image required',
        inputTag: '',
        inputNode: '',
        inputNodeError: 'node required',
        inputRepo: '',
        force_remove: false,
        image: '',
        image_ip: '',
        openModalPrune : false,
        openModalRemove : false,
        TagHost: ''
	};
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
{
    dataField: "action",
    text: "Action"
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

styles_dropdown = {
    container: provided => ({
        ...provided,
        width: 275,
        // float: 'right',
        // position: 'relative'
      }),
    control: base => ({
        ...base,
        color: 'black',
        backgroundColor: 'white',
        borderColor: 'black',
    
        ':hover': {
          borderColor: 'white',
          color: 'black',
        }
    }),
    singleValue: base => ({
        ...base,
        color: "black",
        backgroundColor: 'white',
    }),
    dropdownIndicator: base => ({
        ...base,
        color: "white",
        backgroundColor: 'black',
    }),
    option: base => ({
        ...base,
        color: "black",
        backgroundColor: 'white',

        ':hover': {
            backgroundColor: 'black',
            color: 'white',
          }
    }),
  };

componentDidMount() {
	var self = this;
	imagesService.getImages().then(function (data) {
		self.setState({ images:  data.result})
	});
    nodesService.getNodes().then(function (data) {
        data.result = data.result.filter(host => host.items.Status.State != 'down');
		self.setState({ nodes:  data.result})
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

openNavTag(image) {
    this.setState({
        TagHost: image.host,
        inputImage: image.items.Id
    })
    document.getElementById("tag-sidebar").style.width = "100%";
};

closeNavTag() {
    document.getElementById("tag-sidebar").style.width = "0";
};

closeNavPullImage() {
    document.getElementById("pull-sidebar").style.width = "0";
};

imageHandler = (e) => {
    e.preventDefault();
    this.setState({
        inputImage: e.target.value,
    })
};

imageTagHandler = (e) => {
    e.preventDefault();
    this.setState({
        inputTag: e.target.value,
    })
};

imageRepoHandler = (e) => {
    e.preventDefault();
    this.setState({
        inputRepo: e.target.value,
    })
};

imageNodeHandler = (e) => {
    this.setState({
        inputNode: e.host,
    })
}

handlePullImage(image, tag, node, signal) {
    imagesService.pullImage(image, tag, node, signal)
}

handleSignal(signal) {
	imagesService.pruneImages(signal)
}

imageAction(image) {
    return <div>
        <button id='prune-images' onClick={() => {this.onClickButtonModalDelete(image, 'remove_image')}} className='button button-image-delete'>
            Remove&nbsp;
            <img src={remove_button} className='action-img'/>
        </button>
        <button id='tag-image' onClick={() => {this.openNavTag(image)}} className='button button-image-tag'>
            Tag&nbsp;
            <img src={tag_button} className='action-img'/>
        </button>
        </div>
}

handleDeleteImage(image) {
	imagesService.deleteImage(image)
}

handleTagImage(image, tag, repository, node, signal) {
    imagesService.tagImage(image, tag, repository, node, signal)
}

onClickButtonModalPrune = (signal) => {
    this.setState({
        openModalPrune: true,
        signal: signal,
    })
}

onClickButtonModalDelete = (image, signal) => {
    this.setState({
        openModalRemove: true,
        signal: signal,
        image: image.items.Id,
        image_ip: image.ip,
    })
}

onCloseModalRemove = ()=> {
    this.setState({openModalRemove : false})
}

onCloseModalPrune = ()=> {
    this.setState({openModalPrune : false})
}

handlePreventFormRefresh = () => {
    $("form").on('submit', function (e) {
        e.preventDefault();
        $.get(window.location, $(this).serialize());
     });
}

render() {

    if (this.state.images == 'Unable to collect data. All hosts is unreacheable') {
        return <section className='images-section'>Unable to collect data. All hosts is unreacheable</section>
    }
    return (
            
            <section className='images-section'>
                {/* remove image */}
                <Modal show={this.state.openModalRemove} onHide={this.onCloseModalRemove} dialogClassName="removeConfirm">
                    <Modal.Header closeButton>
                        <Modal.Title>Remove image</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Are you sure you want to remove image: {this.state.image.slice(0, 12)}</Modal.Body>
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
                                this.handleDeleteImage({
                                    'image': this.state.image, 
                                    'image_ip': this.state.image_ip,
                                    'signal': 'remove_image',
                                    'force': document.getElementById('force_checkbox').checked,
                                    })}}>
                                Remove
                            </button>
                    </Modal.Footer>
                </Modal>

                {/* prune images */}
                <Modal show={this.state.openModalPrune} onHide={this.onCloseModalPrune} dialogClassName="removeConfirm">
                    <Modal.Header closeButton>
                        <Modal.Title>Prune images</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Are you sure you want to remove unused images on all hosts</Modal.Body>
                    <Modal.Footer>
                            <button className='button button-modal-prune-cancel' onClick={this.onCloseModalPrune}>
                                Cancel
                            </button>
                            <button className='button button-modal-prune' onClick={() =>{ 
                                this.onCloseModalPrune(); 
                                this.handleSignal({
                                    'signal': this.state.signal,
                                    });}}>
                                Remove
                            </button>
                    </Modal.Footer>
                </Modal>
                
                <div id="tag-sidebar" className="sidenav">
                    <a className="closebtn" onClick={() => {this.closeNavTag()}}>&times;</a>
                    <div className='tag'>
                    <div className='tag-image-block'>
                        <form>
                            <label htmlFor='tag' className='input-tag'>Tag</label>
                            <input onChange={e => this.imageTagHandler(e)} value={this.inputTag} type='text' name='tag'></input><br/>
                            <label htmlFor='tag' className='input-repo'>Repository</label>
                            <input onChange={e => this.imageRepoHandler(e)} value={this.inputRepo} type='text' name='repo'></input><br/>
                            
                            <button 
                            disabled={this.state.inputImage.length<1 || this.state.inputRepo.length<1} 
                            id='tag-image' 
                            className='button button-tag-image' 
                            onClick={() => {
                                this.closeNavTag();  
                                this.handleTagImage(this.state.inputImage, this.state.inputTag, this.state.inputRepo, this.state.TagHost, 'tag_image')}}>
                                Tag the Image&nbsp;
                                <img src={tag_button} className='action-img'/>
                            </button>
                        </form>

                        {this.handlePreventFormRefresh()}

                        </div>
                    <div className='block block-tag'>TAG IMAGE</div>
                    </div>
                </div>

                <div id="pull-sidebar" className="sidenav">
                    <a className="closebtn" onClick={() => {this.closeNavPullImage()}}>&times;</a>
                    <div className='pull'>
                    <div className='pull-image-block'>
                        <form>
                            <label htmlFor='image' className='input-image'>Image</label>
                            {(this.inputImageError) && <div style={{color: 'red'}}>{inputImageError}</div>}
                            <input onChange={e => this.imageHandler(e)} value={this.inputImage} type='text' name='image' ></input><br/>
                            <label htmlFor='tag' className='input-tag'>Tag</label>
                            <input onChange={e => this.imageTagHandler(e)} value={this.inputTag} type='text' name='tag'></input><br/>
                            <Select 
                                onChange={e => this.imageNodeHandler(e)}
                                className="select-host"
                                classNamePrefix="select-host"
                                options={this.state.nodes} 
                                getOptionLabel={(option) => option.host}
                                name="node"
                                styles={this.styles_dropdown}
                                placeholder='Select Node'
                            /><br/>
                            <button 
                            disabled={this.state.inputImage.length<1 || this.state.inputNode.length<1} 
                            id='pull-image' 
                            className='button button-pull-image' 
                            onClick={() => {
                                this.closeNavPullImage(); 
                                this.handlePullImage(this.state.inputImage, this.state.inputTag, this.state.inputNode, 'image_pull')
                                }}>
                                Pull the Image&nbsp;
                                <img src={pull_button} className='action-img'/>
                            </button>
                        </form>

                        {this.handlePreventFormRefresh()}

                        </div>
                    <div className='block block-pull'>PULL IMAGE</div>
                    </div>
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
                    <button id='prune-images' className='button' onClick={()=>{this.onClickButtonModalPrune('prune_images')}}>
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
                                                    <td>{this.state.imageDetails.items.RepoTags.join(', ')}</td>
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
                                            repotags: this.imageDetailsSide(c, c.items.RepoTags.join(', ')),
                                            host: this.imageHostStyle(c.host),
                                            repository: c.items.Repository,
                                            used_by: c.items.Used_by.slice(0, 12),
                                            id: c.items.Id.slice(c.items.Id.indexOf(':')+1, 19),
                                            size: c.items.Size,
                                            created: c.items.Created,
                                            action: this.imageAction(c)
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
