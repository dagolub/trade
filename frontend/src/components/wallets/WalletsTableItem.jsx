import {divClass, buttonView, buttonDelete, tdClass} from '../../utils'
import searchUser from "../searchUser"
import View from '../view'
import showDate from "../showDate";

function WalletTableItem(props) {
    const viewHandler = (id) => {
        window.location.href = "/wallets/view/" + id
    }
    return (
        <tr id={"tr" + props.id}>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{searchUser(props.owner_id)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.wallet}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showDate(props.created)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1" style={{"display": "flex"}}>
                        <button onClick={() => viewHandler(props.id)} className={buttonView}><View /></button>
                </div>
            </td>
        </tr>
    );
}

export default WalletTableItem;