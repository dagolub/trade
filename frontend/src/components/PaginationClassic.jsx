import 'react'
import React

function PaginationClassic({total, settingList}) {
    let hash = parseInt(window.location.hash.split("#")[1])
    hash = hash > 0 ? hash : 0
    const next = hash > 0 ? hash*10 + 10 : 10
    let showTotal = parseInt((hash+1)*10)
    showTotal = showTotal > total ? total : showTotal
    console.log(hash, next, showTotal)
  return (
    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <nav className="mb-4 sm:mb-0 sm:order-1" role="navigation" aria-label="Navigation">
        <ul className="flex justify-center">
            {next > 10 &&
          <li className="ml-3 first:ml-0">
            <a onClick={()=>settingList("", next-20)} className="btn bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:text-slate-300 dark:hover:border-slate-600 text-indigo-500" href={"#"+parseInt(hash-1)}>&lt;- Previous</a>
          </li>}
            {parseInt(hash+1) *10 < total &&
          <li className="ml-3 first:ml-0">
            <a onClick={()=>settingList("", next)} className="btn bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 text-indigo-500" href={"#"+parseInt(hash+1)}>Next -&gt;</a>
          </li>}
        </ul>
      </nav>
      <div className="text-sm text-slate-500 dark:text-slate-400 text-center sm:text-left">
        Showing <span className="font-medium text-slate-600 dark:text-slate-300">{parseInt(hash*10)+1}</span> to <span className="font-medium text-slate-600 dark:text-slate-300">{showTotal}</span>
          {total > 0 &&
          <span> of <span className="font-medium text-slate-600 dark:text-slate-300">{total}</span> results</span>
          }
      </div>
    </div>
  );
}

export default PaginationClassic;
