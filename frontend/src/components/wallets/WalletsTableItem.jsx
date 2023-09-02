import {deleteRow, showError} from "../../utils"; // Replace with the correct path
import React from "react"
import { deleteWallet } from "../../services/api"; // Replace with the correct path
import dayjs from "dayjs"

// import {useAlert} from "react-alert";
function WalletTableItem(props) {
    // const alert = useAlert()

    const deleteHandler = (id) => {
        deleteRow(id)
        setTimeout(() => {
            deleteWallet(id).then((response) => {
                response.wallet ? document.getElementById("tr" + id).remove() : ""
            })
        }, 200)
    }

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
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.owner_id}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.deposit_id}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.wallet}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{props.type}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap td" + props.id}>
                <div className="font-medium text-slate-800 dark:text-slate-100">{dayjs(props.created).format("HH:mm DD MMM YY")}</div>
            </td>
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px td" + props.id}>
                <div className="space-x-1">
                    <a href={"/wallets/edit/" + props.id}>
                        <button
                            className="text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400 rounded-full">
                            <svg className="w-8 h-8 fill-current" viewBox="0 0 32 32">
                                <path
                                    d="M19.7 8.3c-.4-.4-1-.4-1.4 0l-10 10c-.2.2-.3.4-.3.7v4c0 .6.4 1 1 1h4c.3 0 .5-.1.7-.3l10-10c.4-.4.4-1 0-1.4l-4-4zM12.6 22H10v-2.6l6-6 2.6 2.6-6 6zm7.4-7.4L17.4 12l1.6-1.6 2.6 2.6-1.6 1.6z"/>
                            </svg>
                        </button>
                    </a>
                    <button className="text-rose-500 hover:text-rose-600 rounded-full"
                            onClick={() => deleteHandler(props.id)}>
                        <svg className="w-8 h-8 fill-current" viewBox="0 0 32 32">
                            <path d="M13 15h2v6h-2zM17 15h2v6h-2z"/>
                            <path
                                d="M20 9c0-.6-.4-1-1-1h-6c-.6 0-1 .4-1 1v2H8v2h1v10c0 .6.4 1 1 1h12c.6 0 1-.4 1-1V13h1v-2h-4V9zm-6 1h4v1h-4v-1zm7 3v9H11v-9h10z"/>
                        </svg>
                    </button>
                </div>
            </td>
        </tr>
    );
}

export default WalletTableItem;