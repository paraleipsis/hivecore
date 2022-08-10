import React, { Component } from  'react';
import ImagesService  from  '../services/ImagesService';
import Card from 'react-bootstrap/Card';

const  imagesService  =  new  ImagesService();

class  ImagesList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		images: [],
        imageDetails: [],
	};
}

componentDidMount() {
	var self = this;
	imagesService.getImages().then(function (data) {
		self.setState({ images:  data.result})
	});
}

openNav(info) {
    document.getElementById("mySidenav").style.width = "100%";

    this.setState({imageDetails: info})

    var labels = info.items.ContainerConfig.Labels;
    var stringLabels = JSON.stringify(labels).replace(/[{}]/g, '').replace(/["]/g, '').split(',');
    if (stringLabels[0] != '' && stringLabels[0] != 'null') {
        var bodyString = '';
        $.each(stringLabels, function(index, label) {
            bodyString += ('<tr><td>'+label+'</td></tr>');
        });
        $('.image-labels tbody').html(bodyString);
    } else {
        $('.image-labels tbody').html('<tr><td>'+'No labels'+'</td><td>')
    }

    var envs = info.items.Config.Env;
    var bodyString = '';
    $.each(envs, function(index, env) {
        bodyString += ('<tr><td>'+env+'</td></tr>');
    });
    $('.image-env tbody').html(bodyString);

};

closeNav() {
    document.getElementById("mySidenav").style.width = "0";
};

render() {

    return (
            <section className='images-section'>

                <div className="images--list">

                <div id="mySidenav" className="sidenav">

                    <a className="closebtn" onClick={() => {this.closeNav()}}>&times;</a>

                        <Card className='card-info card-image-details'>

                            <Card.Header className='image-info-header'>IMAGE DETAILS</Card.Header>
                            <Card.Body className='image-info'>

                                {/* image details table */}
                                <table id="table-details" className="table table-details" cellPadding="0" cellSpacing="0" border="0">
                                    <thead key="thead" className='tbl-header tbl-header-details'>
                                        <tr>
                                            <th>ID</th>
                                        </tr>
                                        <tr>
                                            <th>Repository</th>
                                        </tr>
                                        <tr>
                                            <th>Container</th>
                                        </tr>
                                        <tr>
                                            <th>Tags</th>
                                        </tr>
                                        <tr>
                                            <th>Size</th>
                                        </tr>
                                        <tr>
                                            <th>Created</th>
                                        </tr>
                                        <tr>
                                            <th>Host</th>
                                        </tr>
                                        <tr>
                                            <th>Docker Version</th>
                                        </tr>
                                        <tr>
                                            <th>OS</th>
                                        </tr>
                                        <tr>
                                            <th>Architecture</th>
                                        </tr>
                                    </thead>

                                    {
                                        this.state.imageDetails.length != 0 && (
                                            <tbody id="tbl-content-details" className='tbl-content tbl-content-details'>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Id}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Repository}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Used_by}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.RepoTags}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Size}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Created}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.host}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.DockerVersion}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Os}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Architecture}</td>
                                                </tr>
                                            </tbody>
                                        )
                                    }

                                </table>

                                {/* image labels table */}
                                <table id="image-labels" className="table image-labels" cellPadding="0" cellSpacing="0" border="0">
                                    <thead key="thead" className='tbl-header'>
                                        <tr>
                                            <th>Labels</th>
                                        </tr>
                                    </thead>
                                    <tbody className='tbl-content'></tbody>
                                </table>

                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        <Card className='card-info card-dockerfile-details'>

                            <Card.Header className='image-info-header'>DOCKERFILE</Card.Header>
                            <Card.Body className='image-info'>

                                {/* image dockerfile table */}
                                <table id="table-details-dockerfile" className="table table-details" cellPadding="0" cellSpacing="0" border="0">
                                    <thead key="thead" className='tbl-header tbl-header-details'>
                                        <tr>
                                            <th>CMD</th>
                                        </tr>
                                        <tr>
                                            <th>ENTRYPOINT</th>
                                        </tr>
                                        <tr>
                                            <th>Exposed Ports</th>
                                        </tr>
                                        <tr>
                                            <th>Volumes</th>
                                        </tr>
                                    </thead>

                                    {
                                        this.state.imageDetails.length != 0 && (
                                            <tbody id="tbl-content-details" className='tbl-content tbl-content-details'>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Config.Cmd}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Config.Entrypoint}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Config.ExposedPorts}</td>
                                                </tr>
                                                <tr>
                                                    <td>{this.state.imageDetails.items.Config.Volumes}</td>
                                                </tr>
                                            </tbody>
                                        )
                                    }
                                    
                                </table>
                                
                                {/* image Env table */}
                                <table className="table image-env" cellPadding="0" cellSpacing="0" border="0">
                                    <thead key="thead" className='tbl-header'>
                                        <tr>
                                            <th>Env</th>
                                        </tr>
                                    </thead>
                                    <tbody className='tbl-content'></tbody>
                                </table>
                                
                            </Card.Body>

                        </Card>

                        <br/>
                        <br/>

                        </div>

                        {/* main images table */}
                        <table id="main-table" className="table main-table" cellPadding="0" cellSpacing="0" border="0">
                            <thead key="thead" className='tbl-header main-table-header'>
                                <tr className='main-table-row'>
                                    <th className='images-main-table-tags-header'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tags</th>
                                    <th className='images-main-table-host-header'>Host</th>
                                    <th>Repository</th>
                                    <th>Container</th>
                                    <th>ID</th>
                                    <th>Size</th>
                                    <th>Created</th>
                                </tr>
                            </thead>

                            <tbody className='tbl-content main-table-content'>
                                {this.state.images.map( c  =>
                                    <tr key={c.items.Id + c.host} className='main-table-row'>
                                    <td><button onClick={() => {this.openNav(c)}} className='button'>{c.items.RepoTags}</button></td>
                                    <td className='images-main-table-host-body'>{c.host}</td>
                                    <td>{c.items.Repository}</td>
                                    <td>{c.items.Used_by.slice(0, 12)}</td>
                                    <td>{c.items.Id.slice(c.items.Id.indexOf(':')+1, 19)}</td>
                                    <td>{c.items.Size}</td>
                                    <td>{c.items.Created}</td>
                                </tr>)}
                            </tbody>
                        </table>

                </div>

            </section>
	);
  }
}

export  default  ImagesList;
