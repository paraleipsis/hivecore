import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Link } from 'react-router-dom';

import NavBar from './components/NavBar'
import Footer from './components/Footer'

import  ImagesList from './dockerapp/views/ImagesList';
import  ContainersList from './dockerapp/views/ContainersList';
import  NetworksList from './dockerapp/views/NetworksList';

import  HomeAnimation from './liquorice/views/home/HomePage';

const BaseLayout = () => (
  <div className="container-fluid">
    <div className="content">
      <Route path="/" exact component={HomeAnimation} />
      <Route path="/images" exact component={ImagesList} />
      <Route path="/containers" exact component={ContainersList} />
      <Route path="/networks" exact component={NetworksList} />
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