import  React, { Component } from  'react';
import  ImagesService  from  './ImagesService';
import { Helmet } from 'react-helmet';
import 'bootstrap/dist/css/bootstrap.css';

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
		console.log(data);
		self.setState({ images:  data.result})
	});
}


render() {

    return (
            <div  className="images--list">
                <table  className="table">
                <thead  key="thead">
                <tr>
                    <th>id</th>
                    <th>tags</th>
                    <th>size</th>
                    <th>created</th>
                    <th>host</th>
                </tr>
                </thead>
                <tbody>
                {this.state.images.map( c  =>
                    <tr  key={c.items.Id + c.host}>
                    <td>{c.items.Id}  </td>
                    <td>{c.items.RepoTags}</td>
                    <td>{c.items.Size}</td>
                    <td>{c.items.Created}</td>
                    <td>{c.host}</td>
                    <td>
                    </td>
                </tr>)}
                </tbody>
                </table>
            </div>
	);

  }
}

export  default  ImagesList;