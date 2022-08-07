import React from "react";
import logo from '../assets/images/favicon.png';
import git_w from '../assets/images/git_icon_white.png';

import { MDBFooter, MDBContainer, MDBRow, MDBCol, MDBIcon } from 'mdb-react-ui-kit';

export default function App() {
  return (
    <MDBFooter bgColor='black' className='footer text-center text-lg-start text-muted fixed-bottom  border-top'>

      <section className='d-flex justify-content-center justify-content-lg-between p-4'>

        <div className='text-white'>
          <p className="footer-logo">
              <img src={logo}  style={{ width: '100px', height: '100px' }}/>
              Liquorice
          </p>
          <div className="border-top footer-copyright">
            Copyright 2022 © by paraleipsis
          </div>
        </div>

        <div>
          <p>
            <a href='https://github.com/paraleipsis/liquorice' target="_blank">
                <button className='button button_git col-md-9'>
                  &nbsp;<img src={git_w}/>
                  GITHUB
                </button>
                
            </a>
          </p>
        </div>

        <div className="text-white">
          <h6 className='text-uppercase fw-bold mb-4'>Contact</h6>
            <p>
              der.krabbentaucher@gmail.com
            </p>
        </div>
      </section>

    </MDBFooter>
  );
}
