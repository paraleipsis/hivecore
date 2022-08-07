import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import NavBar from './components/NavBar'
import Footer from './components/Footer'

import  ImagesList from './dockerapp/views/ImagesList';
import  ContainersList from './dockerapp/views/ContainersList';

import  HomeAnimation from './liquorice/views/home/HomePage';

import './assets/styles.css'

const BaseLayout = () => (
  <div className="container-fluid">
    <div className="content">
      <Route path="/" exact component={HomeAnimation} />
      <Route path="/images" exact component={ImagesList} />
      <Route path="/containers" exact component={ContainersList} />
    </div>
  </div>
  
)

class App extends Component {
  render() {
    return (
        <div className='App'>
            <NavBar/>
            <BrowserRouter>
                <div className='main'>
                    <BaseLayout/>
                </div>
            </BrowserRouter>
            <Footer/>
        </div>
    );
  }
}

export default App;