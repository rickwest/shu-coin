import React, { useState } from "react";
import Transaction from "./Transaction";

function ToggleTransactions({ block }) {
  const [displayTransaction, setDisplayTransaction] = useState(false);

  const toggleDisplay = () => setDisplayTransaction(!displayTransaction);

  if (displayTransaction) {
    return (
      <div>
        {block.data.map(transaction => (
          <div key={transaction.id}>
            <hr />
            <Transaction transaction={transaction} />
          </div>
        ))}
        <button className="btn btn-sm btn-success" onClick={toggleDisplay}>
          Show Less
        </button>
      </div>
    );
  }
  return (
    <div>
      {block.data.length > 0 ? (
        <button className="btn btn-sm btn-success" onClick={toggleDisplay}>
          Show More
        </button>
      ) : null}
    </div>
  );
}

function Block({ block }) {
  const hash = `${block.hash.substring(0, 15)}...`;

  // Divide by 1000000 to convert nanoseconds to milliseconds
  const timestamp = new Date(block.timestamp / 1000000).toLocaleString();

  return (
    <div className="card shadow mb-3">
      <div className="card-body">
        <h5 className="card-title">
          <b>Block Hash:</b> {hash}
        </h5>
        <h6 className="card-subtitle mb-2">
          <span className="font-weight-bold">Timestamp:</span> {timestamp}
        </h6>
        <ToggleTransactions block={block} />
      </div>
    </div>
  );
}

export default Block;
