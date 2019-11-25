import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./components/App";
import { Router, Switch, Route } from "react-router-dom";
import { createBrowserHistory } from "history";
import Blockchain from "./components/Blockchain";
import TransactionForm from "./components/TransactionForm";
import Layout from "./components/Layout";

ReactDOM.render(
  <Router history={createBrowserHistory()}>
    <Switch>
      <Layout>
        <Route path="/" exact component={App} />
        <Route path="/blockchain" component={Blockchain} />
        <Route path="/transaction/new" component={TransactionForm} />
      </Layout>
    </Switch>
  </Router>,
  document.getElementById("root")
);
