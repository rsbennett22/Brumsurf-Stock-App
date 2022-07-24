function setOptions() {
    //Set values for options depending on stockType variable
    //Get elements to add options to
    var brandOptions = document.getElementById('brand');
    var sizeOptions = document.getElementById('size');
    //Check the value of stockType and set options accordingly
    if(stockType.toLowerCase()=='wetsuit'){
        console.log('Wetsuit form page loaded');
        document.getElementById('genderLabel').className='shown';
        document.getElementById('gender').className='shown';
        document.getElementById('gBreak').className='shown';
        //Add options to brand
        createOption(brandOptions, 'oneil');
        createOption(brandOptions, 'twobarefeet');
        createOption(brandOptions, 'tiki');
        //Add options to size
        updateSizeOptions();
    }
    else if(stockType.toLowerCase()=='surfboard') {
        console.log('Surfboard form page loaded');
        //Add options to brand
        createOption(brandOptions, 'hotsurf');
        createOption(brandOptions, 'bic');
        createOption(brandOptions, 'surfworx');
        //...//
        //Add options to size
        createOption(sizeOptions, "6'0");
        createOption(sizeOptions, "7'0");
        createOption(sizeOptions, "8'0");
    }
    else if(stockType.toLowerCase()=='surfskate') {
        console.log('Surfboard form page loaded');
        //Add options to brand
        createOption(brandOptions, 'slide');
        createOption(brandOptions, 'yow');
        createOption(brandOptions, 'carver');
        //...//
        //Hide size option
        document.getElementById('size').className='hidden';
        document.getElementById('sizeLabel').className='hidden';
        document.getElementById('sBreak').className='hidden';
    }
    else if(stockType.toLowerCase()=='boot') {
        console.log('Boots form page loaded');
        //Add options to brand
        createOption(brandOptions, 'cskin');
        createOption(brandOptions, 'oneil');
        //...//
        //Set size options
        for(i=1; i<=12; i++) {
            createOption(sizeOptions, i.toString())
        }
        //Hide number option
        document.getElementById('num').className='hidden'
        document.getElementById('numLabel').className='hidden'
        //Show amount option
        document.getElementById('amount').className='shown'
        document.getElementById('amountLabel').className='shown'
    }
    else if(stockType.toLowerCase()=='glove') {
        console.log('Gloves form page loaded');
        //Add options to brand
        createOption(brandOptions, 'cskin');
        createOption(brandOptions, 'oneil');
        //...//
        //Set size options
        createOption(sizeOptions, 'small');
        createOption(sizeOptions, 'medium');
        createOption(sizeOptions, 'large');
        createOption(sizeOptions, 'x-large');
        //Hide number option
        document.getElementById('num').className='hidden'
        document.getElementById('numLabel').className='hidden'
        //Show amount option
        document.getElementById('amount').className='shown'
        document.getElementById('amountLabel').className='shown'
    }
    else {
        console.log('Hoods form page loaded');
        //Add options to brand
        createOption(brandOptions, 'cskin');
        createOption(brandOptions, 'oneil');
        //...//
        //Set size options
        createOption(sizeOptions, 'small');
        createOption(sizeOptions, 'medium');
        createOption(sizeOptions, 'large');
        createOption(sizeOptions, 'x-large');
        //Hide number option
        document.getElementById('num').className='hidden'
        document.getElementById('numLabel').className='hidden'
        //Show amount option
        document.getElementById('amount').className='shown'
        document.getElementById('amountLabel').className='shown'
    }
}
function createOption(parent, value) {
    var newOption = document.createElement('option');
    newOption.value = value;
    newOption.innerHTML = value;
    parent.appendChild(newOption);
}
function updateSizeOptions() {
    const sizesMale = ['small', 'medium', 'medium-tall', 'large', 'x-large'];
    const sizesFemale = ['4', '6', '8', '10', '12', '14', '16'];
    //get the gender select field's selected value
    var genderField = document.getElementById('gender');
    var sizeField = document.getElementById('size');
    var gender = genderField.value;
    console.log(gender)
    var optionsTotal = sizeField.length;
    //check if any options present
    if(optionsTotal!=0) {
        //remove options present
        for(i=0; i<=optionsTotal-1; i++) {
            //remove option 0 from select field
            sizeField.remove(0);
        }
    }
    //check what gender is selected
    if(gender=='male') {
        //add options for male sizes
        for(i=0; i<=sizesMale.length-1; i++) {
            createOption(sizeField, sizesMale[i])
        }
    }
    else {
        //add options for female sizes
        for(i=0; i<=sizesFemale.length-1; i++) {
            createOption(sizeField, sizesFemale[i])
        }
    }
}