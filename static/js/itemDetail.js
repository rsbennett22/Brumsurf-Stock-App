function setCurrentUrl(id){
    console.log(id)
    document.getElementById(id).value=location.href
}
function setDefaultsAndReload() {
    if(stockType=='wetsuit') {
        //Unhide gender header
        document.getElementById('gender').className='shown'
    }
    if(stockType=='surfskate') {
        //Unhide gender header
        document.getElementById('size').className='hidden'
    }
    //Get status of item, signedIn, signedOut and onTrip and disable/enable buttons accordingly
    
    //Set relevant buttons based on values of above vars
    if(signedIn=='True') {
        //Get sign in button and disable it
        document.getElementById('signIn').disabled = true;
    }
    else if(onTrip=='True' || signedOut=='True') {
        document.getElementById('onTrip').disabled = true;
        document.getElementById('signOut').disabled = true;
    }
    if(window.location.href == 'http://192.168.0.58:8000/addNewItem/') {
        if("{{stockType}}"=='wetsuit') {
            url = 'http://192.168.0.58:8000/detail/wetsuit&'+number
            window.location.replace(url)
        }
        else if("{{stockType}}"=='surfboard') {
            url = 'http://192.168.0.58:8000/detail/surfboard&'+number
            window.location.replace(url)
        }
    }
}
function showHideSignOutOptions(element) {
    nameField = document.getElementById('studentName');
    nameLabel = document.getElementById('nameLabel');
    idField = document.getElementById('studentId');
    idLabel = document.getElementById('idLabel')
    if(element.checked) {
        //Show input fields for name and id
        nameField.style.display = 'block';
        nameLabel.style.display = 'block';
        idField.style.display = 'block';
        idLabel.style.display = 'block';
    }
    else {
        //Hide elements
        nameField.style.display = 'none';
        nameLabel.style.display = 'none';
        idField.style.display = 'none';
        idLabel.style.display = 'none';
        //Clear fields
        nameField.value=''
        idField.value=''
    }
}