import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";

function App() {
  const [walletInfo, setWalletInfo] = useState({});

  useEffect(() => {
    fetch(`${API_BASE_URL}/wallet/show`)
      .then(response => response.json())
      .then(json => setWalletInfo(json));
  }, []);

  const { address, balance } = walletInfo;
  return (
    <div>
      <p className="lead">
        <span className="font-weight-bold">Wallet Address:</span>&nbsp;
        {address}
      </p>
      <p className="lead">
        <span className="font-weight-bold">Balance:</span>&nbsp;{balance}{" "}
        <small className="text-muted">SHU</small>
      </p>
    </div>
  );
}

export default App;
