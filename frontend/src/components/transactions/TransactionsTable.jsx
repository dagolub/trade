import './TransactionsTableItem.jsx';
import React, {useState, useEffect} from 'react';
import Transaction from './TransactionsTableItem';
import {getUserMe} from "../../services/api"; // Correct path to your TransactionsTableItem component

function TransactionTable({
                              list,
                              settingList
                          }) {
    const [superuser, setSuperuser] = React.useState(false)
    React.useEffect(() => {
        getUserMe().then((data) => setSuperuser(data["is_superuser"]))
    })
    return (
        <div
            className="bg-white dark:bg-slate-800 shadow-lg rounded-sm border border-slate-200 dark:border-slate-700 relative">
            <div>
                <div className="overflow-x-auto">
                    <table className="table-auto w-full dark:text-slate-300">
                        <thead
                            className="text-xs font-semibold uppercase text-slate-500 dark:text-slate-400 bg-slate-50 dark:bg-slate-900/20 border-t border-b border-slate-200 dark:border-slate-700">
                        <tr>
                            {superuser && <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">User</div>
                            </th>}
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">From wallet</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">To wallet</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Tx</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Amount</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Fee</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Currency</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Created</div>
                            </th>

                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Act</div>
                            </th>
                        </tr>
                        </thead>
                        {/* Table body */}
                        <tbody className="text-sm divide-y divide-slate-200 dark:divide-slate-700">
                        {

                            list.map(entity => {
                                return (
                                    <Transaction
                                        key={entity.id}
                                        id={entity.id}

                                        from_wallet={entity.from_wallet}
                                        to_wallet={entity.to_wallet}
                                        tx={entity.tx}
                                        amount={entity.amount}
                                        fee={entity.fee}
                                        currency={entity.currency}
                                        type={entity.type}
                                        created={entity.created}
                                        withdraw_id={entity.withdraw_id}
                                        owner_id={entity.owner_id}
                                        superuser={superuser}

                                        settingList={settingList}
                                    />
                                )
                            })
                        }
                        </tbody>
                    </table>

                </div>
            </div>
        </div>
    );
}

export default TransactionTable;