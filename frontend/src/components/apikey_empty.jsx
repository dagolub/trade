import {putApikeys} from "../services/api";
const ApiKEYEmpty = () => {
    const generate = () => {
        putApikeys([]).then((data)=> {
            window.location.href = window.location.href
        })
    }
    return (
        <div className="apiKEY">
            <button className="btn bg-indigo-500 hover:bg-indigo-600 text-white" style={{"margin": "10px"}}
                    type="submit" onClick={generate}>
                 Generate KEY
            </button>
        </div>
    )
}

export default ApiKEYEmpty;