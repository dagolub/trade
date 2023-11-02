import Banner from "./Banner";
function showError (data){
    //console.log(data)
    if (data.hasOwnProperty("response")) {
        return (<Banner  type="error">123</Banner>)
        //alert(data.response.data.detail)
    }
}

export default showError;