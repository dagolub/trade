import React from 'react';
import Sidebar from '../../partials/Sidebar';
import Header from '../../partials/Header';
import Form from '../../components/users/form'; // Corrected import path

function UsersNew() {
  return (
    <div className="flex h-[100vh] overflow-hidden"> {/* Fixed typo in height */}
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form />
          </div>
        </main>
      </div>
    </div>
  );
}

export default UsersNew;
