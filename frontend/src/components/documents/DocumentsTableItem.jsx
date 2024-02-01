import {deleteDocument} from '../../services/api'
import {divClass, buttonView, buttonDelete, tdClass, deleteEnt} from '../../utils'
import searchUser from "../searchUser"
import Del from '../delete'
import Edit from '../edit'
import showDate from "../showDate";

function DocumentsTableItem(props) {
    const editHandler = (id) => {
        window.location.href = "/documents/edit/" + id
    }
    const deleteHandler = (id) => {
        deleteEnt(deleteDocument, id)
    };

    return (
        <tr id={"tr" + props.id}>
            {props.superuser && <td className={tdClass(props.id)}>
                <div className={divClass}>{searchUser(props.owner_id)}</div>
            </td>}
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.name}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.file}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.ext}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showDate(props.created)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1" style={{"display": "flex"}}>
                    <button onClick={() => editHandler(props.id)} className={buttonView}><Edit/></button>
                    <button onClick={() => deleteHandler(props.id)} className={buttonDelete}><Del/></button>
                </div>
            </td>
        </tr>
    );
}

export default DocumentsTableItem;
