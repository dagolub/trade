import {deleteDeposit} from '../../services/api'
import {showWallet, divClass, buttonView, buttonDelete, tdClass, deleteEntity} from '../../utils'
import searchUser from "../searchUser"
import showWalletCopy from "../showWalletCopy"
import Del from '../delete'
import View from '../view'
import showDate from "../showDate";
function DepositTableItem(props) {
const viewHandler = (id) => {
    window.location.href = "/deposits/view/" + id
}
const deleteHandler = (id) => {
    deleteEntity(deleteDeposit, id)
};

    return (
        <tr id={"tr" + props.id}>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{searchUser(props.owner_id)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showWallet(props.wallet)}{showWalletCopy(props.wallet)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.sum}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.paid}</div>
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
                <div className="space-x-1" style={{"display": "flex"}}>
                    <button onClick={() => viewHandler(props.id)} className={buttonView}><View /></button>
                    <button onClick={() => deleteHandler(props.id)} className={buttonDelete}><Del /></button>
                </div>
            </td>
        </tr>
    );
}

export default DepositTableItem;
