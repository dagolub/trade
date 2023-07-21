import React from 'react';
import {
  Routes,
  Route,
  useLocation
} from 'react-router-dom';

import './css/style.css';
import Dashboard from "./pages/dashboard";
import Users from './pages/users/list';
import UsersNew from './pages/users/new';
import UsersEdit from './pages/users/edit';


import Deposits from './pages/deposits/list';
import DepositsNew from './pages/deposits/new';
import DepositsEdit from './pages/deposits/edit';


import Transactions from './pages/transactions/list';
import TransactionsNew from './pages/transactions/new';
import TransactionsEdit from './pages/transactions/edit';


import Wallets from './pages/wallets/list';
import WalletsNew from './pages/wallets/new';
import WalletsEdit from './pages/wallets/edit';

//INSERT_1


import Signin from './pages/Signin';


function App() {

  const location = useLocation();

  React.useEffect(() => {
    document.querySelector('html').style.scrollBehavior = 'auto'
    window.scroll({ top: 0 })
    document.querySelector('html').style.scrollBehavior = ''
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
//INSERT_2
        <Route path="/signin" element={<Signin />} />
      </Routes>
    </>
  );
}

export default App;