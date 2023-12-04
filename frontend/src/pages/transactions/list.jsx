import React from 'react'
import Header from '../../partials/Header'
import PaginationClassic from '../../components/PaginationClassic'
import SearchForm from '../../partials/actions/SearchForm'
import Sidebar from '../../partials/Sidebar'
import TransactionsTable from '../../components/transactions/TransactionsTable'
import {getTransactions} from '../../services/api'
import {getEntities, setTot} from "../../utils"

function Transactions() {
  const [list, setList] = React.useState([]);
  const [total, setTotal] = React.useState(0);
    const settingList = () => {
        getEntities(getTransactions, setList)
    };

    React.useEffect(() => {
        settingList()
        setTot('transactions', setTotal)
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
                <SearchForm placeholder="Search by from wallet" />
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
            <TransactionsTable list={list} settingList={settingList} />
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
