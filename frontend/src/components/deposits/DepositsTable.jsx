import React, { useState, useEffect } from 'react';
import Deposit from './DepositsTableItem'; // Correct path to your Deposit component

function DepositTable({
  selectedItems,
  list,
  settingList
}) {
  const [selectAll, setSelectAll] = useState(false);
  const [isCheck, setIsCheck] = useState([]);

  const handleSelectAll = () => {
    setSelectAll(!selectAll);
    setIsCheck(selectAll ? [] : list.map(li => li.id));
  };

  const handleClick = e => {
    const { id, checked } = e.target;
    setSelectAll(false);
    setIsCheck(prevIsCheck =>
      checked ? [...prevIsCheck, id] : prevIsCheck.filter(item => item !== id)
    );
  };

  useEffect(() => {
    selectedItems(isCheck);
  }, [isCheck, selectedItems]);

  return (
    <div className="bg-white dark:bg-slate-800 shadow-lg rounded-sm border border-slate-200 dark:border-slate-700 relative">
      <header className="px-5 py-4">
        <h2 className="font-semibold text-slate-800 dark:text-slate-100">Deposits <span className="text-slate-400 dark:text-slate-500 font-medium">1</span></h2>
      </header>
      <div>
        {/* Table */}
        <div className="overflow-x-auto">
          <table className="table-auto w-full dark:text-slate-300">
            {/* Table header */}
            <thead className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-900/20 border-t border-b border-slate-200 dark:border-slate-700">
              <tr>
                <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px">
                  <div className="flex items-center">
                    <label className="inline-flex">
                      <span className="sr-only">Select all</span>
                      <input className="form-checkbox" checked={selectAll} onChange={handleSelectAll} />
                    </label>
                  </div>
                </th>
                {/* ... Other th elements ... */}
              </tr>
            </thead>
            {/* Table body */}
            <tbody className="text-sm divide-y divide-slate-200 dark:divide-slate-700">
              {list.map(entity => (
                <Deposit
                  key={entity.id}
                  id={entity.id}
                  wallet={entity.wallet}
                  type={entity.type}
                  sum={entity.sum}
                  currency={entity.currency}
                  status={entity.status}
                  handleClick={handleClick}
                  isChecked={isCheck.includes(entity.id)}
                  settingList={settingList}
                />
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default DepositTable;
