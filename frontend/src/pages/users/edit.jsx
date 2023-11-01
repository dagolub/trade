import React, { useState, useEffect } from 'react';
import Sidebar from '../../partials/Sidebar';
import Form from '../../components/users/form';
import Header from '../../partials/Header';
import { getUser, getOTP } from '../../services/api';
import { useParams } from 'react-router-dom';
import {showError} from '../../utils'

function UsersEdit() {
  const { id } = useParams();
  const [full_name, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [is_active, setIsActive] = useState(false);
  const [is_superuser, setIsSuperUser] = useState(false);
  const [autotransfer, setAutoTransfer] = useState(false);

  useEffect(() => {
    getUser(id)
      .then((data) => {
          setFullName(data.full_name);
          setEmail(data.email);
          setIsActive(data.is_active);
          setIsSuperUser(data.is_superuser);
          setAutoTransfer(data.autotransfer);
      })
      .catch((error) => {
        showError(error);
      });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form
              name={full_name}
              email={email}
              is_active={is_active}
              is_superuser={is_superuser}
              auto={autotransfer}
              id={id}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default UsersEdit;
