import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";
import { history } from "../index";

function TransactionForm() {
  const [amount, setAmount] = useState(0);
  const [recipientAddress, setRecipientAddress] = useState("");
  const [hasError, setHasError] = useState(false);
  const [knownAddresses, setKnownAddresses] = useState([]);

  const submitTransaction = () => {
    if (!amount > 0 || !recipientAddress.trim()) {
      setHasError(true);
      return;
    }

    fetch(`${API_BASE_URL}/wallet/transaction`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ recipient_address: recipientAddress, amount })
    })
      .then(response => response.json())
      .then(json => {
        alert("Transaction submitted successfully!");
        history.push("/transaction/pool");
      });
  };

  useEffect(() => {
    fetch(`${API_BASE_URL}/blockchain/addresses`)
      .then(response => response.json())
      .then(json => setKnownAddresses(json));
  }, []);

  return (
    <div className="transaction-form">
      <h3 className="mb-4">New Transaction</h3>
      {hasError ? (
        <div className="alert alert-danger">
          <strong>Error!</strong> You must enter a recipient wallet address and
          an amount greater than 0.
        </div>
      ) : null}

      <div className="form-group">
        <input
          type="text"
          className="form-control"
          id="recipient-input"
          placeholder="Enter recipient wallet address..."
          value={recipientAddress}
          onChange={event => {
            setRecipientAddress(event.target.value.trim());
            setHasError(false);
          }}
          required={true}
        />
      </div>
      <div className="form-group">
        <input
          type="number"
          className="form-control"
          id="amount-input"
          placeholder="Enter number of SHU's to send..."
          value={amount}
          onChange={event => {
            setAmount(Number(event.target.value));
            setHasError(false);
          }}
          required={true}
        />
      </div>
      <button
        type="submit"
        className="btn btn-success"
        onClick={submitTransaction}
      >
        Submit
      </button>
      <hr className="mb-4 mt-4" />
      <div>
        <h5>Known Wallet Addresses</h5>
        {knownAddresses.map((address, index) => (
          <span key={address} className="small text-muted">
            {address}
            {index !== knownAddresses.length - 1 ? " | " : ""}
          </span>
        ))}
      </div>
    </div>
  );
}

export default TransactionForm;
