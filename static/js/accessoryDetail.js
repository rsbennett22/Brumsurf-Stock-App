function setDefaultsAndReload() {
    document.getElementById('updateTheAmount').checked=false
    if(window.location.href == 'http://192.168.0.58:8000/addNewItem/') {
        if("{{stockType}}"=='boot') {
            url = 'http://192.168.0.58:8000/detail/'+pk
            window.location.replace(url)
        }
    }
}
function showHideAmountUpdate(element) {
    amountLabel = document.getElementById('newAmountLabel')
    amountField = document.getElementById('newAmount')
    if(element.checked) {
        amountLabel.className='shown';
        amountField.className='shown';
    }
    else {
        amountLabel.className='hidden';
        amountField.className='hidden';
    }
}
function setUrl() {
    newAmount = document.getElementById('newAmount').value
    newUpdateUrl = updateUrl+'&'+newAmount.toString()
    document.updateAmount.action = newUpdateUrl
}