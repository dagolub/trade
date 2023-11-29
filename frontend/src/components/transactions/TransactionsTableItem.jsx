import {showWallet, divClass, buttonView, tdClass} from '../../utils'
import searchUser from "../searchUser"
import showWalletCopy from "../showWalletCopy"
import View from '../view'
import showDate from "../showDate";

function TransactionTableItem(props) {
    const viewHandler = (id) => {
        window.location.href = "/transactions/view/" + id
    }
    return (
        <tr id={"tr" + props.id}>
            {props.superuser && <td className={tdClass(props.id)}>
                <div className={divClass}>{searchUser(props.owner_id)}</div>
            </td>}
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showWallet(props.from_wallet)}{showWalletCopy(props.from_wallet)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showWallet(props.to_wallet)}{showWalletCopy(props.to_wallet)}</div>

            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showWallet(props.tx)}{showWalletCopy(props.tx)}</div>

            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.withdraw_id && props.amount > 0? "-" : ""}{props.amount}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.fee}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.currency}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showDate(props.created)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1" style={{"display": "flex"}}>
                    <button onClick={() => viewHandler(props.id)} className={buttonView}><View/></button>
                </div>
            </td>
        </tr>
    );
}

export default TransactionTableItem;