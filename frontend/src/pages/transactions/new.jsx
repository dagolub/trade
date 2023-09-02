import React from 'react';
import Sidebar from '../../partials/Sidebar';
import Form from '../../components/transactions/form';

function TransactionsNew() {
  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form />
          </div>
        </main>
      </div>
    </div>
  );
}

export default TransactionsNew;
