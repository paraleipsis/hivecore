import  React, { Component } from  'react';
import 'bootstrap/dist/css/bootstrap.css';
import sketch from './animation.js';
import { ReactP5Wrapper } from "react-p5-wrapper";

class  Animation  extends  Component {

render() {

    return (
        <div  className="animation">
            <ReactP5Wrapper sketch={sketch}/>
            <div className="main_info">Visualize | Monitor | Control</div>
        </div>
	);

  }
}

export  default  Animation;