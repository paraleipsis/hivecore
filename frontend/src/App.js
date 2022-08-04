import React, { Component } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

import NavBar from './components/NavBar'
import Footer from './components/Footer'
import  ImagesList from './ImagesList';
import  Animation from './Animation_render';

import './styles.css'

const BaseLayout = () => (
  <div className="container-fluid">
    <div className="content">
      <Route path="/" exact component={Animation} />
      <Route path="/images" exact component={ImagesList} />
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