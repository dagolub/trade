import React from 'react'
function Currency({currency, amount}) {


  return (
    <div style={{"height": "120px"}} className="flex flex-col col-span-full sm:col-span-6 xl:col-span-4 bg-white dark:bg-slate-800 shadow-lg rounded-sm border border-slate-200 dark:border-slate-700">
      <div className="px-5 pt-5">

        <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-2">{currency}</h2>

        <div className="flex items-start">
          <div className="text-3xl font-bold text-slate-800 dark:text-slate-100 mr-2">{amount}</div>

        </div>
      </div>

    </div>
  );
}

export default Currency;
