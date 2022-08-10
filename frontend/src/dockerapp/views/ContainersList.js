import  React, { Component } from  'react';
import  ContainersService  from  '../services/ContainersService';
import Card from 'react-bootstrap/Card';

const  containersService  =  new ContainersService();


class  ContainersList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		containers: [],
	};
}

componentDidMount() {
	var self = this;
	containersService.getContainers().then(function (data) {
		self.setState({ containers:  data.result})
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
        console.log(p_ports)
        return p_ports
    }
    return '-';
}

render() {

    return (
            <section className='containers-section'>

                <div id="main" className="containers--list">

                        {/* sidebar with specific container details */}
                        <div id="mySidenav" className="sidenav">

                            <a className="closebtn" onClick={() => {this.closeNav()}}>&times;</a>

                            <Card className='card-info card-container-details'>

                                <Card.Header className='container-info-header'>CONTAINER DETAILS</Card.Header>
                                <Card.Body className='container-info'>

                                    {/* container details table */}
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

                                    {/* container labels table */}
                                    <table id="container-labels" className="table container-labels" cellPadding="0" cellSpacing="0" border="0">
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
                        
                        {/* main containers table */}
                        <table id="main-table" className="table main-table" cellPadding="0" cellSpacing="0" border="0">
                            <thead key="thead" className='tbl-header main-table-header'>
                                <tr className='main-table-row'>
                                    <th className='images-main-table-tags-header'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Name</th>
                                    <th className='images-main-table-host-header'>Host</th>
                                    <th>Status</th>
                                    <th>Image</th>
                                    <th>IP Address</th>
                                    <th>Ports</th>
                                    <th>Created</th>
                                </tr>
                            </thead>

                            <tbody className='tbl-content main-table-content'>
                                {this.state.containers.map( c  =>
                                    <tr key={c.items.Id + c.host} className='main-table-row'>
                                    <td>
                                        <button onClick={() => {this.openNav(c)}} className='button'>
                                            {c.items.Name.length > 20 ? c.items.Name.slice(0, 20) + ' ...' : c.items.Name}
                                        </button>
                                    </td>
                                    <td className='images-main-table-host-body'>{c.host}</td>
                                    <td>{c.items.State.Status}</td>
                                    <td>{c.items.Config.Image.indexOf("@") > -1 ? c.items.Config.Image.slice(0, c.items.Config.Image.indexOf('@')) : c.items.Config.Image}</td>
                                    <td>{Object.values(c.items.NetworkSettings.Networks)[0]['IPAddress'] != '' ? Object.values(c.items.NetworkSettings.Networks)[0]['IPAddress'] : '-'}</td>
                                    <td>{this.container_ports(c.items.NetworkSettings.Ports)}</td>
                                    <td>{c.items.Created.replace('T', ' ').slice(0, c.items.Created.indexOf('.'))}</td>
                                </tr>)}
                            </tbody>
                        </table>
                </div>
            </section>
	);

  }
}

export  default  ContainersList;