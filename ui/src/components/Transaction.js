import React from "react";

function Transaction({ transaction }) {
  const { input, output } = transaction;

  return (
    <div>
      <p className="card-text">
        <span className="font-weight-bold">From:</span> {input.address}
      </p>
      {Object.keys(output).map(recipient => (
        <p key={recipient} className="card-text">
          <span className="font-weight-bold">To:</span> {recipient} |{" "}
          <span className="font-weight-bold">Sent:</span> {output[recipient]}{" "}
          <span className="text-muted">SHU</span>
        </p>
      ))}
    </div>
  );
}

export default Transaction;
