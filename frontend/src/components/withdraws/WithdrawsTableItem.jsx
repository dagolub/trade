import React from "react"
import dayjs from "dayjs"
import {deleteRow} from "../../utils";
import {deleteWithdraw} from "../../services/api";

function WalletTableItem(props) {
    const viewHandler = (id) => {
        window.location.href = "/withdraws/view/" + id
    }
    const deleteHandler = (id) => {
        deleteRow(id);
        setTimeout(() => {
            deleteWithdraw(id).then((response) => {
                if (response.status) {
                    document.getElementById("tr" + id).remove();
                }
            });
        }, 200);
    };

    return (
        <tr id={"tr" + props.id}>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px td" + props.id}>
                <div className="flex items-center">
                    <label className="inline-flex">
                        <span className="sr-only">Select</span>
                        <input id={props.id} className="form-checkbox" type="checkbox" onChange={props.handleClick}
                               checked={props.isChecked}/>
                    </label>
                </div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.sum}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.to}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.currency}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.chain}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.status}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div
                    className="font-medium text-slate-800 dark:text-slate-100">{dayjs(props.created).format("HH:mm DD MMM YY")}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px td" + props.id}>
                <div className="space-x-1">
                    <div className="space-x-1" style={{"display": "flex"}}>
                        <button onClick={() => viewHandler(props.id)}
                            className="text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400 rounded-full">
                            <svg fill="#64748b" height="20px" width="20px" viewBox="0 0 80.794 80.794">
                                <g>
                                    <g>
                                        <path d="M79.351,38.549c-0.706-0.903-17.529-22.119-38.953-22.119c-21.426,0-38.249,21.216-38.955,22.119L0,40.396l1.443,1.847
                                        c0.706,0.903,17.529,22.12,38.955,22.12c21.424,0,38.247-21.217,38.953-22.12l1.443-1.847L79.351,38.549z M40.398,58.364
                                        c-15.068,0-28.22-13.046-32.643-17.967c4.425-4.922,17.576-17.966,32.643-17.966c15.066,0,28.218,13.045,32.642,17.966
                                        C68.614,45.319,55.463,58.364,40.398,58.364z"/>
                                        <path d="M40.397,23.983c-9.052,0-16.416,7.363-16.416,16.414c0,9.053,7.364,16.417,16.416,16.417s16.416-7.364,16.416-16.417
                                        C56.813,31.346,49.449,23.983,40.397,23.983z M40.397,50.813c-5.744,0-10.416-4.673-10.416-10.417
                                        c0-5.742,4.672-10.414,10.416-10.414c5.743,0,10.416,4.672,10.416,10.414C50.813,46.14,46.14,50.813,40.397,50.813z"/>
                                    </g>
                                </g>
                            </svg>
                        </button>
                        <button className="text-rose-500 hover:text-rose-600 rounded-full"
                                onClick={() => deleteHandler(props.id)}>
                            <svg className="w-8 h-8 fill-current" viewBox="0 0 32 32">
                                <path d="M13 15h2v6h-2zM17 15h2v6h-2z"/>
                                <path
                                    d="M20 9c0-.6-.4-1-1-1h-6c-.6 0-1 .4-1 1v2H8v2h1v10c0 .6.4 1 1 1h12c.6 0 1-.4 1-1V13h1v-2h-4V9zm-6 1h4v1h-4v-1zm7 3v9H11v-9h10z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </td>
        </tr>
    );
}

export default WalletTableItem;