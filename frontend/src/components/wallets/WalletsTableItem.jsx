import React from "react"
import dayjs from "dayjs"

function WalletTableItem(props) {
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
                    <a href={"/wallets/view/" + props.id}>
                        <button
                            className="text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400 rounded-full">
                            <svg fill="#FFFFFF" height="20px" width="20px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg"
                                 viewBox="0 0 80.794 80.794">
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
                    </a>
                </div>
            </td>
        </tr>
    );
}

export default WalletTableItem;