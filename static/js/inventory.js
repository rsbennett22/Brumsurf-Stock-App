function saveCSV() {
	//Get all item info
	/*console.log(wetsuitArray);
	console.log(surfboardArray);
	console.log(surfskateArray);
	console.log(bootArray);
	console.log(gloveArray);
	console.log(hoodArray);
	*/

	//Format data into CSV format
	fmtd_Wetsuits = format(wetsuitArray, 'wetsuit');
	fmtd_Surfboards = format(surfboardArray, 'surfboard');
	fmtd_Surfskates = format(surfskateArray, 'surfskate');
	fmtd_Boots = format(bootArray, 'boots');
	fmtd_Gloves = format(gloveArray, 'gloves');
	fmtd_Hoods = format(hoodArray, 'hoods');
	/*
	console.log(fmtd_Wetsuits);
	console.log(fmtd_Surfboards);
	console.log(fmtd_Surfskates);
	console.log(fmtd_Boots);
	console.log(fmtd_Gloves);
	console.log(fmtd_Hoods);
	*/
	//Collate all data
	csvData = combine(fmtd_Wetsuits, fmtd_Surfboards, fmtd_Surfskates, fmtd_Boots, fmtd_Gloves, fmtd_Hoods);
	//console.log(csvData);

	//Export data as a file
	csvContent = "data:text/csv;charset=utf-8," + csvData;
	var encodedUri = encodeURI(csvContent);
	var link = document.createElement("a");
	link.setAttribute("href", encodedUri);
	link.setAttribute("download", "inventory.csv");
	document.body.appendChild(link)
	link.click();
}
function format(array, type) {
	formattedData='';
	if(type=='wetsuit')
	{
		//iterate over entire array
		for(let i=0; i<array.length; i++) {
			//Add each element to formattedData
			let wet = array[i];
			formattedData += wet.brand+','+wet.gender+','+wet.size+','+wet.wetsuitNumber+','+wet.onTrip+','+wet.signedOut+','+wet.signedIn+','+wet.name+','+wet.studentId;
			//Add a newline
			formattedData += '\r\n';
		}
		return formattedData;
	}
	else if(type=='surfboard')
	{
		//iterate over entire array
		for(let i=0; i<array.length; i++) {
			//Add each element to formattedData
			let surf = array[i];
			formattedData += surf.brand+','+surf.size+','+surf.surfboardNumber+','+surf.onTrip+','+surf.signedOut+','+surf.signedIn+','+surf.name+','+surf.studentId;
			//Add a surf
			formattedData += '\r\n';
		}
		return formattedData;
	}
	else if(type=='surfskate')
	{
		//iterate over entire array
		for(let i=0; i<array.length; i++) {
			//Add each element to formattedData
			let surf = array[i];
			formattedData += surf.brand+','+surf.surfskateNumber+','+surf.onTrip+','+surf.signedOut+','+surf.signedIn+','+surf.name+','+surf.studentId;
			//Add a surf
			formattedData += '\r\n';
		}
		return formattedData;
	}
	else
	{
		//iterate over entire array
		for(let i=0; i<array.length; i++) {
			//Add each element to formattedData
			let accessory = array[i];
			formattedData += accessory.brand+','+accessory.size+','
			if(type=='boots')
			{
				formattedData += accessory.bootAmount;
			}
			else if(type=='gloves') {
				formattedData += accessory.gloveAmount;
			}
			else {
				formattedData += accessory.hoodAmount;
			}
			//Add a surf
			formattedData += '\r\n';
		}
		return formattedData;
	}
}
function combine(wetsuits, surfboards, surfskates, boots, gloves, hoods) {
	combined=''
	//Set headings for tables
	wetsuitHeadings = 'Brand, Gender, Size, Number,On Trip, Signed Out, Signed In, Name, Student Id\n';
	surfboardHeadings = 'Brand, Size, Number, On Trip, Signed Out, Signed In, Name, Student Id\n';
	surfskateHeadings = 'Brand, Number, On Trip, Signed Out, Signed In, Name, Student Id\n';
	accessoryHeadings = 'Brand, Size, Amount\n';

	//Append data together
	combined += 'Wetsuits\n' + wetsuitHeadings + wetsuits + '\n'
			 + 'Surfboards\n' + surfboardHeadings + surfboards + '\n'
			 + 'Surfskates\n' + surfskateHeadings + surfskates + '\n'
			 + 'Boots\n' + accessoryHeadings + boots + '\n'
			 + 'Gloves\n' + accessoryHeadings + gloves + '\n'
			 + 'Hoods\n' + accessoryHeadings + hoods;
	return combined
}