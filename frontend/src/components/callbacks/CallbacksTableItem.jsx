import {showWallet, divClass, buttonView, tdClass} from "../../utils";
import searchUser from "../searchUser";
import showDate from "../showDate";
import View from '../view'
import showWalletCopy from "../showWalletCopy"

function CallbackTableItem(props) {
    const viewHandler = (id) => {
        window.location.href = "/callback/view/" + id
    }
    return (
        <tr id={"tr" + props.id}>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{searchUser(props.owner_id)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showWallet(props.callback)}{showWalletCopy(props.callback)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>
                    <a href={"/deposits/view/" + props.deposit_id} style={{"textDecoration": "underline"}}>
                        {props.deposit_id}
                    </a>
                </div>
            </td>
            <td className={tdClass(props.id)}>
                <a href={"/withdraws/view/" + props.withdraw_id} style={{"textDecoration": "underline"}}>
                    <div className={divClass}>{props.withdraw_id}</div>
                </a>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showDate(props.created)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1">
                    <button onClick={() => viewHandler(props.id)} className={buttonView}><View/></button>
                </div>
            </td>
        </tr>
    );
}

export default CallbackTableItem;