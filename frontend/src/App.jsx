import React, { useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Dashboard from './pages/dashboard'; // Import Dashboard properly
import Deposits from './pages/deposits/list'; // Import Deposits properly
import DepositsEdit from './pages/deposits/edit'; // Import DepositsEdit properly
import DepositsNew from './pages/deposits/new'; // Import DepositsNew properly
import Settings from './pages/settings'; // Import Settings properly
import Transactions from './pages/transactions/list'; // Import Transactions properly
import TransactionsEdit from './pages/transactions/edit'; // Import TransactionsEdit properly
import TransactionsNew from './pages/transactions/new'; // Import TransactionsNew properly
import Users from './pages/users/list'; // Import Users properly
import UsersEdit from './pages/users/edit'; // Import UsersEdit properly
import UsersNew from './pages/users/new'; // Import UsersNew properly
import Wallets from './pages/wallets/list'; // Import Wallets properly
import WalletsEdit from './pages/wallets/edit'; // Import WalletsEdit properly
import WalletsNew from './pages/wallets/new'; // Import WalletsNew properly
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
        <Route path="/deposits/edit/:id" element={<DepositsEdit />} />
        <Route path="/transactions/list" element={<Transactions />} />
        <Route path="/transactions/new" element={<TransactionsNew />} />
        <Route path="/transactions/edit/:id" element={<TransactionsEdit />} />
        <Route path="/wallets/list" element={<Wallets />} />
        <Route path="/wallets/new" element={<WalletsNew />} />
        <Route path="/wallets/edit/:id" element={<WalletsEdit />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/signin" element={<Signin />} />
      </Routes>
    </>
  );
}

export default App;
