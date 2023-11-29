import React, {useState, useEffect} from 'react';
import Withdraw from './WithdrawsTableItem';
import {getUserMe} from "../../services/api"; // Make sure to provide the correct path

function WalletTable({
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
                                <div className="font-semibold text-left">Sum</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Fee</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">To</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Currency</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Chain</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Status</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Created</div>
                            </th>
                            <th className="px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap">
                                <div className="font-semibold text-left">Actions</div>
                            </th>
                        </tr>
                        </thead>
                        {/* Table body */}
                        <tbody className="text-sm divide-y divide-slate-200 dark:divide-slate-700">
                        {

                            list.map(entity => {
                                return (
                                    <Withdraw
                                        key={entity.id}
                                        id={entity.id}

                                        sum={entity.sum}
                                        to={entity.to}
                                        currency={entity.currency}
                                        chain={entity.chain}
                                        status={entity.status}
                                        created={entity.created}
                                        owner_id={entity.owner_id}
                                        fee={entity.fee}
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

export default WalletTable;