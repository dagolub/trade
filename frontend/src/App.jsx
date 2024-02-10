import React, { useEffect } from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import Dashboard from './pages/dashboard'

import Users from './pages/users/list'
import UsersNew from './pages/users/new'
import UsersEdit from './pages/users/edit'

import Documents from './pages/documents/list'
import DocumentsNew from './pages/documents/new'
import DocumentsEdit from './pages/documents/edit'

import Folders from './pages/folders/list'
import FoldersNew from './pages/folders/new'
import FoldersEdit from './pages/folders/edit'

import Pages from './pages/pages/list'
import PagesNew from './pages/pages/new'
import PagesEdit from './pages/pages/edit'

import Settings from './pages/settings'

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

        <Route path="/documents/list" element={<Documents />} />
        <Route path="/documents/new" element={<DocumentsNew />} />
        <Route path="/documents/edit/:id" element={<DocumentsEdit />} />

        <Route path="/folders/list" element={<Folders />} />
        <Route path="/folders/new/" element={<FoldersNew />} />
        <Route path="/folders/edit/:id" element={<FoldersEdit />} />

        <Route path="/pages/list" element={<Pages />} />
        <Route path="/pages/new/" element={<PagesNew />} />
        <Route path="/pages/edit/:id" element={<PagesEdit />} />

        <Route path="/settings" element={<Settings />} />
        <Route path="/signin" element={<Signin />} />

      </Routes>
    </>
  );
}

export default App;
