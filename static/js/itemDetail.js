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
        document.getElementById('studentSignOut').disabled = true;
        document.getElementById('onTrip').disabled = true;
        document.getElementById('signOut').disabled = true;
    }
    if(window.location.href == 'http://192.168.0.75:8000/addNewItem/') {
        if(stockType=='wetsuit') {
            url = 'http://192.168.0.75:8000/detail/wetsuit&'+number;
            window.location.replace(url);
        }
        else if(stockType=='surfboard') {
            url = 'http://192.168.0.75:8000/detail/surfboard&'+number
            window.location.replace(url)
        }
        else {
            url = 'http://192.168.0.75:8000/detail/surfskate&'+number
            window.location.replace(url)
        }
    }
}
function showHideSignOutOptions(element) {
    nameField = document.getElementById('studentName');
    nameLabel = document.getElementById('nameLabel');
    idField = document.getElementById('studentId');
    idLabel = document.getElementById('idLabel');
    nameBreak = document.getElementById('nameBreak');
    checkBreak = document.getElementById('checkBreak');
    signoutBreak = document.getElementById('signoutBreak');
    fieldSplit = document.getElementById('fieldSplit');
    if(element.checked) {
        //Show input fields for name and id
        nameField.className='shown';
        nameLabel.className='shown';
        idField.className='shown';
        idLabel.className='shown';
        nameBreak.className='shown';
        checkBreak.className='shown';
        signoutBreak.className='shown';
        fieldSplit.className='shown';
    }
    else {
        //Hide elements
        nameField.className='hidden';
        nameLabel.className='hidden';
        idField.className='hidden';
        idLabel.className='hidden';
        nameBreak.className='hidden';
        checkBreak.className='hidden';
        signoutBreak.className='hidden';
        fieldSplit.className='hidden';
        //Clear fields
        nameField.value=''
        idField.value=''
    }
}