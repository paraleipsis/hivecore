import React from 'react';

import {
  MDBContainer,
  MDBNavbar,
  MDBNavbarBrand,
  MDBNavbarNav,
  MDBNavbarItem,
  MDBNavbarLink,
  MDBCollapse,
} from 'mdb-react-ui-kit';

import NavDropdown from 'react-bootstrap/NavDropdown';

function NavBar() {
  return (
    <MDBNavbar expand='lg' dark bgColor='black' className="fixed-top">
      <MDBContainer fluid>
        <MDBNavbarBrand href='/' className='nav-brand'>Liquorice |</MDBNavbarBrand>
        <MDBCollapse navbar >
          <MDBNavbarNav>

            <MDBNavbarItem>
            <div className="dropdown">
              <button className='button'>Images</button>
              <div className="dropdown-options">
                <a href='/images'><button className='button'>Image List</button></a>
                <a href='/build_image'><button className='button'>Build Image</button></a>
                <a href='/pull_image'><button className='button'>Pull Image</button></a>
              </div>
            </div>
            </MDBNavbarItem>
            
            <MDBNavbarItem>
            <div className="dropdown">
              <button className='button'>Containers</button>
              <div className="dropdown-options">
                <a href='/containers'><button className='button'>Container List</button></a>
                <a href='/build_image'><button className='button'>Create Container</button></a>
                <a href='/pull_image'><button className='button'>&Compose&</button></a>
              </div>
            </div>
            </MDBNavbarItem>

            <MDBNavbarItem>
            <div className="dropdown">
              <button className='button'>Networks</button>
              <div className="dropdown-options">
                <a href='/networks'><button className='button'>Network List</button></a>
                <a href='/build_image'><button className='button'>Create Network</button></a>
                <a href='/pull_image'><button className='button'>Plugin List</button></a>
              </div>
            </div>
            </MDBNavbarItem>

            <MDBNavbarItem>
            <div className="dropdown">
              <button className='button'>Volumes</button>
              <div className="dropdown-options">
                <a href='/volumes'><button className='button'>Volume List</button></a>
                <a href='/build_image'><button className='button'>Create Volume</button></a>
                <a href='/pull_image'><button className='button'>Plugin List</button></a>
              </div>
            </div>
            </MDBNavbarItem>

            

            
            
          </MDBNavbarNav>
        </MDBCollapse>
      </MDBContainer>
    </MDBNavbar>
  );
}

export default NavBar;