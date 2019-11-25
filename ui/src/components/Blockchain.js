import React, { useState, useEffect } from "react";
import { API_BASE_URL } from "../config";
import Block from "./Block";

const PAGE_RANGE = 5;

function Blockchain() {
  const [blockchain, setBlockchain] = useState([]);
  const [blockchainLength, setBlockchainLength] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);

  const fetchBlockchainPage = ({ start, end }) => {
    setCurrentPage(start / PAGE_RANGE);

    fetch(`${API_BASE_URL}/blockchain?s=${start}&e=${end}`)
      .then(response => response.json())
      .then(json => setBlockchain(json));
  };

  useEffect(() => {
    fetchBlockchainPage({ start: 0, end: PAGE_RANGE });

    fetch(`${API_BASE_URL}/blockchain/length`)
      .then(response => response.json())
      .then(json => setBlockchainLength(json));
  }, []);

  const buttons = [];
  for (let i = 0; i < blockchainLength / PAGE_RANGE; i++) {
    buttons.push(i);
  }

  return (
    <div className="blockchain">
      <h3 className="mb-4">SHUcoin Blockchain</h3>

      {blockchain.map(block => (
        <Block key={block.hash} block={block} />
      ))}
      <nav>
        <ul className="pagination">
          {buttons.map(number => (
            <li
              key={number}
              className={`page-item ${currentPage === number ? "active" : ""}`}
              onClick={() => {
                fetchBlockchainPage({
                  start: number * PAGE_RANGE,
                  end: (number + 1) * PAGE_RANGE
                });
              }}
            >
              <a className="page-link" href="#">
                {number + 1}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

export default Blockchain;
