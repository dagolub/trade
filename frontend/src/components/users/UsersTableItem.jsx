import {deleteEntity} from '../../utils'
import {deleteUser} from '../../services/api'
import {buttonView, tdClass, divClass, buttonDelete} from '../../utils'
import Delete from "../delete"
import Edit from "../edit"
import typeIcon from "../typeIcon";
function UsersTableItem(props) {
    const deleteHandler = (id) => {
        deleteEntity(deleteUser(), id)
    };

    const editHandler = (id) => {
        window.location.href = "/users/edit/" + id
    };

    return (
        <tr id={"tr" + props.id}>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.full_name}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className={divClass}>{props.email}</div>
            </td>
            <td className={tdClass(props.id)}>
                {typeIcon(props.is_active)}
                <div>{props.is_active}</div>
            </td>
            <td className={tdClass(props.id)}>
                {typeIcon(props.is_superuser)}
                <div>{props.is_superuser}</div>
            </td>
            <td className={tdClass(props.id)}>
                {typeIcon(props.autotransfer)}
                <div>{props.autotransfer}</div>
            </td>
            <td className={tdClass(props.id)}>
                <div className="space-x-1">
                    <button onClick={() => editHandler(props.id)} className={buttonView}><Edit /></button>
                    <button onClick={() => deleteHandler(props.id)} className={buttonDelete}><Delete /></button>
                </div>
            </td>
        </tr>
    );
}

export default UsersTableItem;
