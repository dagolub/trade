import React, { useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Dashboard from './pages/dashboard'; // Import Dashboard properly
import Deposits from './pages/deposits/list'; // Import Deposits properly
import DepositsNew from './pages/deposits/new'; // Import Deposits properly
import DepositsView from './pages/deposits/view'; // Import DepositsEdit properly

import Settings from './pages/settings'; // Import Settings properly

import Transactions from './pages/transactions/list'; // Import Transactions properly
import TransactionsView from './pages/transactions/view'; // Import TransactionsNew properly

import Users from './pages/users/list'; // Import Users properly
import UsersEdit from './pages/users/edit'; // Import UsersEdit properly
import UsersNew from './pages/users/new'; // Import UsersNew properly

import Wallets from './pages/wallets/list'; // Import Wallets properly
import WalletsView from './pages/wallets/view'; // Import WalletsNew properly

import Withdraws from './pages/withdraws/list'; // Import Wallets properly
import WithdrawsNew from './pages/withdraws/new'; // Import Wallets properly
import WithdrawsView from './pages/withdraws/view'; // Import WalletsNew properly
import Callbacks from './pages/callbacks/list'; // Import Wallets properly
import CallbacksView from './pages/callbacks/view'; // Import WalletsNew properly
import Signin from './pages/Signin'; // Import Signin properly
import './css/style.css';

function App() {
  const location = useLocation();

  useEffect(() => {
    document.querySelector('html').style.scrollBehavior = 'auto';
    window.scroll({ top: 0 });
    document.querySelector('html').style.scrollBehavior = '';
  }, [location.pathname]); // triggered on route change

  return (
    <>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/users/list" element={<Users />} />
        <Route path="/users/new" element={<UsersNew />} />
        <Route path="/users/edit/:id" element={<UsersEdit />} />

        <Route path="/deposits/list" element={<Deposits />} />
        <Route path="/deposits/new" element={<DepositsNew />} />
        <Route path="/deposits/view/:id" element={<DepositsView />} />


        <Route path="/transactions/list" element={<Transactions />} />ew
        <Route path="/transactions/view/:id" element={<TransactionsView />} />

        <Route path="/wallets/list" element={<Wallets />} />
        <Route path="/wallets/view/:id" element={<WalletsView />} />

        <Route path="/withdraws/list" element={<Withdraws />} />
        <Route path="/withdraws/new" element={<WithdrawsNew />} />
        <Route path="/withdraws/new?sum=:sum" element={<WithdrawsNew />} />
        <Route path="/withdraws/view/:id" element={<WithdrawsView />} />

        <Route path="/callbacks/list" element={<Callbacks />} />
        <Route path="/callbacks/view/:id" element={<CallbacksView />} />

        <Route path="/settings" element={<Settings />} />
        <Route path="/signin" element={<Signin />} />
      </Routes>
    </>
  );
}

export default App;
