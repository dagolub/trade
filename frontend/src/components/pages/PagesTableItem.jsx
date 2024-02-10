import {divClass, buttonView, buttonDelete, tdClass, deleteEnt} from '../../utils'
import searchUser from "../searchUser"
import Edit from '../edit'
import Del from '../delete'
import showDate from "../showDate";
import {deleteFolder} from "../../services/api";

function FoldersTableItem(props) {
    const editHandler = (id) => {
        window.location.href = "/folders/edit/" + id
    }
    const deleteHandler = (id) => {
        deleteEnt(deleteFolder, id)
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
                <div className={divClass}>{props.folder_id}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{showDate(props.created)}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1" style={{"display": "flex"}}>
                    <button onClick={() => editHandler(props.id)} className={buttonView}><Edit/></button>
                    <button onClick={() => deleteHandler(props.id)} className={buttonView}><Del/></button>
                </div>
            </td>
        </tr>
    );
}

export default FoldersTableItem;