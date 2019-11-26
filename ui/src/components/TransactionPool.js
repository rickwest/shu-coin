import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";
import Transaction from "./Transaction";
import { history } from "../index";

function TransactionPool() {
  const [transactions, setTransactions] = useState([]);

  const fetchTransactions = () => {
    fetch(`${API_BASE_URL}/transactions`)
      .then(response => response.json())
      .then(json => setTransactions(json));
  };

  const mineBlock = () => {
    fetch(`${API_BASE_URL}/blockchain/mine`).then(() => {
      alert("Block mined successfully!");
      history.push("/blockchain");
    });
  };

  useEffect(() => {
    fetchTransactions();

    const intervalId = setInterval(fetchTransactions, 10000); // Fetch transactions every 10 seconds.

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="transaction-pool">
      <h3 className="mb-4">Transaction Pool</h3>

      {transactions.map(transaction => (
        <div key={transaction.id}>
          <Transaction key={transaction.id} transaction={transaction} />
          <hr />
        </div>
      ))}
      {/*eslint-disable-next-line*/}
      <button className="btn btn-success" onClick={mineBlock}>
        Mine a block of these transactions ⛏️
      </button>
    </div>
  );
}

export default TransactionPool;
