import React, { useState, useEffect } from "react";
import logo from "../assets/logo.png";
import { API_BASE_URL } from "../config";
import Blockchain from "./Blockchain";

function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/show`)
      .then(response => response.json())
      .then(json => setWalletInfo(json));
  }, []);

  const { address, balance } = walletInfo;
  return (
    <div className="container p-3 text-center text-break">
      <div className="row justify-content-center">
        <div className="col-md-auto">
          <img className="img-fluid" src={logo} alt="SHUcoin logo" />
          <div className="mt-4 mb-4">
            <p className="lead">
              <span className="font-weight-bold">Wallet Address:</span>&nbsp;
              {address}
            </p>
            <p className="lead">
              <span className="font-weight-bold">Balance:</span>&nbsp;{balance}{" "}
              <small className="text-muted">SHU</small>
            </p>
          </div>
          <hr />
          <Blockchain />
        </div>
      </div>
    </div>
  );
}

export default App;
