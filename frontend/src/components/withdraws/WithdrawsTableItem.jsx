import {showWallet, divClass, buttonView, buttonDelete, tdClass, deleteEnt} from '../../utils'
import searchUser from "../searchUser"
import showWalletCopy from "../showWalletCopy"
import Del from '../delete'
import View from '../view'
import showDate from "../showDate";
import {deleteWithdraw} from "../../services/api";

function WalletTableItem(props) {
    const viewHandler = (id) => {
        window.location.href = "/withdraws/view/" + id
    }
    const deleteHandler = (id) => {
        deleteEnt(deleteWithdraw, id)
    };

    return (
        <tr id={"tr" + props.id}>
            {props.superuser && <td className={tdClass(props.id)}>
                <div className={divClass}>{searchUser(props.owner_id)}</div>
            </td>}
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.sum}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.fee}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showWallet(props.to)}{showWalletCopy(props.to)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.currency}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.chain}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.status}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showDate(props.created)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1">
                    <div className="space-x-1" style={{"display": "flex"}}>
                        <button onClick={() => viewHandler(props.id)} className={buttonView}><View/></button>
                        <button onClick={() => deleteHandler(props.id)} className={buttonDelete}><Del/></button>
                    </div>
                </div>
            </td>
        </tr>
    );
}

export default WalletTableItem;