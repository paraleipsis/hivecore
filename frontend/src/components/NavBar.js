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

function NavBar() {
  return (
    <MDBNavbar expand='lg' dark bgColor='black' className="fixed-top">
      <MDBContainer fluid>
        <MDBNavbarBrand href='/'>Liquorice</MDBNavbarBrand>
        <MDBCollapse navbar >
          <MDBNavbarNav>

            <MDBNavbarItem>
            <a href='/images'><button className='button'>Images</button></a>
            </MDBNavbarItem>
            
            <MDBNavbarItem>
              <a href='/'><button className='button'>Features</button></a>
            </MDBNavbarItem>
            
          </MDBNavbarNav>
        </MDBCollapse>
      </MDBContainer>
    </MDBNavbar>
  );
}

export default NavBar;