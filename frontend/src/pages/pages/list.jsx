import React from 'react'
import Sidebar from '../../partials/Sidebar'
import Header from '../../partials/Header'
import SearchForm from '../../partials/actions/SearchForm'
import PaginationClassic from '../../components/PaginationClassic'
import PagesTable from '../../components/pages/PagesTable'
import {getPages} from '../../services/api'
import {getEntities, setTot} from "../../utils"
import New from "../../components/new";

function Pages() {
  const [list, setList] = React.useState([]);
  const [total, setTotal] = React.useState(0);

    const settingList = () => {
        getEntities(getPages, setList)
    };

    React.useEffect(() => {
        settingList()
        setTot('pages', setTotal)
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
                <h1 className="text-2xl md:text-3xl text-slate-800 dark:text-slate-100 font-bold">Pages ✨</h1>
              </div>
              <div className="grid grid-flow-col sm:auto-cols-max justify-start sm:justify-end gap-2">
                <SearchForm placeholder="Search by title"/>
                <a href="/pages/new">
                  <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white">
                    <New/>
                    <span className="hidden xs:block ml-2">Create page</span>
                  </button>
                </a>
              </div>
            </div>
            <div className="sm:flex sm:justify-between sm:items-center mb-5">
              <div className="mb-4 sm:mb-0">
                <ul className="flex flex-wrap -m-1">
                  <li className="m-1">
                    <button
                        className="inline-flex items-center justify-center text-sm font-medium leading-5 rounded-full px-3 py-1 border border-transparent shadow-sm bg-indigo-500 text-white duration-150 ease-in-out">
                      All <span className="ml-1 text-indigo-200">{total}</span>
                    </button>
                  </li>
                </ul>
              </div>
            </div>
            <PagesTable list={list} settingList={settingList} />
            <div className="mt-8">
              <PaginationClassic total={total} settingList={settingList} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Pages;
