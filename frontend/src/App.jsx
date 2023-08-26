import 'react'
import React
import {

  Routes,
  Route,
  useLocation
} from 'react-router-dom';

import "./pages/dashboard"
import './css/style.css'
import './pages/deposits/edit'
import './pages/deposits/list'
import './pages/deposits/new'
import './pages/settings'
import './pages/transactions/edit'
import './pages/transactions/list'
import './pages/transactions/new'
import './pages/users/edit'
import './pages/users/list'
import './pages/users/new'
import './pages/wallets/edit'
import './pages/wallets/list'
import './pages/wallets/new'
import Dashboard
import Deposits
import DepositsEdit
import DepositsNew
import Settings
import Transactions
import TransactionsEdit
import TransactionsNew
import Users
import UsersEdit
import UsersNew
import Wallets
import WalletsEdit
import WalletsNew

//INSERT_1


import './pages/Signin'
import Signin

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

        <Route path="/settings" element={<Settings />} />
//INSERT_2
        <Route path="/signin" element={<Signin />} />
      </Routes>
    </>
  );
}

export default App;