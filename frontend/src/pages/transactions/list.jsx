import React, { useState, useEffect } from 'react';
import Header from '../../partials/Header'; // Corrected import
import PaginationClassic from '../../components/PaginationClassic'; // Corrected import
import SearchForm from '../../partials/actions/SearchForm'; // Corrected import
import Sidebar from '../../partials/Sidebar'; // Corrected import
import TransactionsTable from '../../components/transactions/TransactionsTable'; // Corrected import
import { getTransactions, GET } from '../../services/api'; // Corrected import

function Transactions() {
  const [selectedItems, setSelectedItems] = useState([]);
  const [list, setList] = useState([]);
  const [total, setTotal] = useState(0);

  const handleSelectedItems = (selectedItems) => {
    setSelectedItems([...selectedItems]);
  };

  const settingList = (q = '', count) => {
    setTimeout(() => {
      const q = document.location.search.split('=')[1];
      getTransactions(q, count).then((data) => setList(data));
    }, 500);
  };

  useEffect(() => {
    let hash = parseInt(window.location.hash.split('#')[1]);
    hash = hash > 0 ? hash : 0;

    let q = document.location.search.split('=')[1];
    getTransactions(q, hash * 10).then((data) => setList(data));

    q = document.location.search.split('=')[1];
    if (q) {
        GET('/api/transactions/count?q=' + q).then((data) => setTotal(data));
    } else {
        GET('/api/transactions/count').then((data) => setTotal(data));
    }
  }, []);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <div className="sm:flex sm:justify-between sm:items-center mb-5">
              <div className="mb-4 sm:mb-0">
                <h1 className="text-2xl md:text-3xl text-slate-800 dark:text-slate-100 font-bold">Transactions ✨</h1>
              </div>
              <div className="grid grid-flow-col sm:auto-cols-max justify-start sm:justify-end gap-2">
                <SearchForm placeholder="Search by user ID…" />
              </div>
            </div>
            <div className="sm:flex sm:justify-between sm:items-center mb-5">
              <div className="mb-4 sm:mb-0">
                <ul className="flex flex-wrap -m-1">
                  <li className="m-1">
                    <button className="inline-flex items-center justify-center text-sm font-medium leading-5 rounded-full px-3 py-1 border border-transparent shadow-sm bg-indigo-500 text-white duration-150 ease-in-out">All <span className="ml-1 text-indigo-200">{total}</span></button>
                  </li>
                </ul>
              </div>
            </div>
            <TransactionsTable selectedItems={handleSelectedItems} list={list} settingList={settingList} />
            <div className="mt-8">
              <PaginationClassic total={total} settingList={settingList} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Transactions;
