import React from 'react';
import {deleteDeposit} from '../../services/api'; // Correct path to your API service
import {deleteRow} from '../../utils'; // Correct path to your utility function

function DepositTableItem(props) {
    const deleteHandler = (id) => {
        deleteRow(id);
        setTimeout(() => {
            deleteDeposit(id).then((response) => {
                if (response.wallet) {
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
                        <input id={props.id} className="form-checkbox" type="checkbox" onChange={props.handleClick} checked={props.isChecked} />
                    </label>
                </div>
            </td>
            {/* ... Other table cells ... */}
            <td className={"px-2 first:pl-5 last:pr-5 py-3 whitespace-nowrap w-px td" + props.id}>
                <div className="space-x-1">
                    <a href={"/deposits/edit/" + props.id}>
                        <button className="text-slate-400 hover:text-slate-500 dark:text-slate-500 dark:hover:text-slate-400 rounded-full">
                            {/* Edit icon */}
                        </button>
                    </a>
                    <button className="text-rose-500 hover:text-rose-600 rounded-full" onClick={() => deleteHandler(props.id)}>
                        {/* Delete icon */}
                    </button>
                </div>
            </td>
        </tr>
    );
}

export default DepositTableItem;
