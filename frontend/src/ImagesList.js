import  React, { Component } from  'react';
import  ImagesService  from  './ImagesService';
import 'bootstrap/dist/css/bootstrap.css';
import Card from 'react-bootstrap/Card';

const  imagesService  =  new  ImagesService();



class  ImagesList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		images: [],
	};
}


componentDidMount() {
	var  self  =  this;
	imagesService.getImages().then(function (data) {
		self.setState({ images:  data.result})
	});
}

openNav(info) {
    document.getElementById("mySidenav").style.width = "100%";
    document.getElementById('image-id').innerHTML = info.items.Id;
    document.getElementById('image-repo').innerHTML = info.items.Repository;
    document.getElementById('image-container').innerHTML = info.items.Used_by;
    document.getElementById('image-tags').innerHTML = info.items.RepoTags;
    document.getElementById('image-size').innerHTML = info.items.Size;
    document.getElementById('image-created').innerHTML = info.items.Created;
    document.getElementById('image-host').innerHTML = info.host;
    document.getElementById('image-docker-version').innerHTML = info.items.DockerVersion;
    document.getElementById('image-os').innerHTML = info.items.Os;
    document.getElementById('image-architecture').innerHTML = info.items.Architecture;

    var labels = info.items.ContainerConfig.Labels;
    var stringLabels = JSON.stringify(labels).replace(/[{}]/g, '').replace(/["]/g, '').split(',');
    console.log(stringLabels)
    if (stringLabels[0] != '' && stringLabels[0] != 'null') {
        var bodyString = '';
        $.each(stringLabels, function(index, label) {
            bodyString += ('<tr><td>'+label+'</td><td>');
        });
        $('.image-labels tbody').html(bodyString);
    } else {
        $('.image-labels tbody').html('<tr><td>'+'No labels'+'</td><td>')
    }

    document.getElementById('image-cmd').innerHTML = info.items.Config.Cmd;
    document.getElementById('image-entrypoint').innerHTML = info.items.Config.Entrypoint;
    document.getElementById('image-exposedports').innerHTML = info.items.Config.ExposedPorts;
    document.getElementById('image-volumes').innerHTML = info.items.Config.Volumes;

    var envs = info.items.Config.Env;
    // var stringLabels = JSON.stringify(labels).replace(/[{}]/g, '').replace(/["]/g, '').split(',');
    var bodyString = '';
    $.each(envs, function(index, env) {
        bodyString += ('<tr><td>'+env+'</td><td>');
    });
    $('.image-env tbody').html(bodyString);

};

  closeNav() {
    document.getElementById("mySidenav").style.width = "0";
};

AutoWidthColumns() {
    $(window).resize(function() {}).resize(); 
}

render() {

    return (
            <section className='images-section'>
                <div id="main" className="images--list">

                        <div id="mySidenav" className="sidenav">
                            <a className="closebtn" onClick={() => {this.closeNav()}}>&times;</a>
                            <Card className='card-info'>
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

                                        <tbody className='tbl-content tbl-content-details'>
                                            <tr>
                                                <td id='image-id'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-repo'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-container'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-tags'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-size'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-created'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-host'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-docker-version'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-os'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-architecture'></td>
                                            </tr>
                                        </tbody>

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
                                    {/* <Card.Title>ID</Card.Title>
                                    <Card.Text id='image-info'></Card.Text> */}
                                </Card.Body>
                            </Card>
                            <br/>
                            <br/>
                            <Card className='card-info'>
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

                                        <tbody className='tbl-content tbl-content-details'>
                                            <tr>
                                                <td id='image-cmd'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-entrypoint'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-exposedports'></td>
                                            </tr>
                                            <tr>
                                                <td id='image-volumes'></td>
                                            </tr>
                                        </tbody>

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
                                    {/* <Card.Title>ID</Card.Title>
                                    <Card.Text id='image-info'></Card.Text> */}
                                </Card.Body>
                            </Card>
                            <br/>
                            <br/>
                        </div>
                        
                        
                        {/* main images table */}
                        <table id="main-images-table" className="table main-images-table" cellPadding="0" cellSpacing="0" border="0">
                            <thead key="thead" className='tbl-header main-images-header'>
                                <tr className='main-images-row'>
                                    <th className='images-main-table-tags-header'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Tags</th>
                                    <th className='images-main-table-host-header'>Host</th>
                                    <th>Repository</th>
                                    <th>Container</th>
                                    <th>ID</th>
                                    <th>Size</th>
                                    <th>Created</th>
                                </tr>
                            </thead>

                            <tbody className='tbl-content main-images-content'>
                                {this.state.images.map( c  =>
                                    <tr key={c.items.Id + c.host} className='main-images-row'>
                                    <td><button onClick={() => {this.openNav(c)}} className='button'>{c.items.RepoTags}</button></td>
                                    <td className='images-main-table-host-body'>{c.host}</td>
                                    <td>{c.items.Repository}</td>
                                    <td>{c.items.Used_by.slice(0, 12)}</td>
                                    <td>{c.items.Id.slice(c.items.Id.indexOf(':')+1, 19)}</td>
                                    <td>{c.items.Size}</td>
                                    <td className='main-images-created-data'>{c.items.Created}</td>
                                </tr>)}
                            </tbody>
                        </table>
                        {this.AutoWidthColumns()}
                </div>
            </section>
	);

  }
}

export  default  ImagesList;