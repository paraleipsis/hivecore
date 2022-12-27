import React, { Component } from "react";
import "xterm/dist/xterm.css";
import { Terminal } from "xterm";
import * as attach from "xterm/lib/addons/attach/attach";

Terminal.applyAddon(attach);

class TerminalApp extends Component {
  async componentDidMount() {
    const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
    let socketURL = protocol + "localhost" + ":8003"

    const term = new Terminal({});
    term.open(this.termElm);

    
    const socket = new WebSocket(socketURL);

    socket.addEventListener('error', (event) => {
      console.log('WebSocket error: ', event);
    });

    socket.onopen = () => {
      term.attach(socket);
      term._initialized = true;
    };
    this.term = term;
  }

  render() {
    return (
    <section className='terminal-section'>
      <div id="main" className="terminal">
        <div style={{ padding: "10px" }}>
          <div ref={(ref) => (this.termElm = ref)}></div>
        </div>
      </div>
      <div className='block'>TERMINAL</div>
    </section>
    );
  }
}

export default TerminalApp;

