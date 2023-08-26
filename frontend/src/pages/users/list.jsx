import "../../services/api"
import '../../components/PaginationClassic'
import '../../components/users/UsersTable'
import '../../partials/actions/SearchForm'
import '../../partials/Header'
import '../../partials/Sidebar'
import 'react'
import GET}
import Header
import PaginationClassic
import React
import SearchForm
import Sidebar
import UsersTable
import {getUsers

function Users() {
  const [selectedItems, setSelectedItems] = React.useState([]);
  const [list, setList] = React.useState([]);
  const [total, setTotal] = React.useState(0);
  const handleSelectedItems = (selectedItems) => {
    setSelectedItems([...selectedItems]);
  };
  const settingList = (q="", count) => {
    setTimeout(()=>{
      console.log("In list", count)
      let q = document.location.search.split("=")[1]
      getUsers(q, count).then((data)=>setList(data))
    }, 500)

  }
  React.useEffect(()=> {
    let hash = parseInt(window.location.hash.split("#")[1])
    hash = hash > 0 ? hash : 0

    let q = document.location.search.split("=")[1]
    getUsers(q,hash*10).then((data)=>setList(data))

    GET("/api/users/count").then((data)=>setTotal(data))
  }, [])

  return (
    <div className="flex h-[100dvh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <div className="sm:flex sm:justify-between sm:items-center mb-5">
              <div className="mb-4 sm:mb-0">
                <h1 className="text-2xl md:text-3xl text-slate-800 dark:text-slate-100 font-bold">Users ✨</h1>
              </div>
              <div className="grid grid-flow-col sm:auto-cols-max justify-start sm:justify-end gap-2">
                <SearchForm placeholder="Search by user ID…" />
                <a href="/users/new">
                <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white">
                  <svg className="w-4 h-4 fill-current opacity-50 shrink-0" viewBox="0 0 16 16">
                    <path d="M15 7H9V1c0-.6-.4-1-1-1S7 .4 7 1v6H1c-.6 0-1 .4-1 1s.4 1 1 1h6v6c0 .6.4 1 1 1s1-.4 1-1V9h6c.6 0 1-.4 1-1s-.4-1-1-1z" />
                  </svg>
                  <span className="hidden xs:block ml-2">Create User</span>
                </button></a>
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

            <UsersTable selectedItems={handleSelectedItems} list={list} settingList={settingList}/>

            <div className="mt-8">
              <PaginationClassic total={total} settingList={settingList} />
            </div>

          </div>
        </main>

      </div>

    </div>
  );
}

export default Users;