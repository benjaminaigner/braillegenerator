
//diameter of the braille dot (might be adjusted for your printer, 1.44 is according to the standard)
const diameter = 1.44;
//resolution for circle rendering
const resolution = 8;
//thickness of the back plate
const plate_thickness = 2;
//how many rows are used (might be changed to e.g. 4 for "PC braille")
const col_size = 3;
//which braille dialect will be used?
//Note: only 0 is valid currently (german)
const brailledialect = 'german';

// Here we define the user editable parameters:
function getParameterDefinitions() {
  return [
    { name: 'supportPlate', caption: 'Nutze eine Support Platte für leichteres Drucken:', type: 'bool', default: true },
    { name: 'backPlate', caption: 'Drucke Braille auf einer 2mm Platte:', type: 'bool', default: true },
    { name: 'text', caption: 'Braille Text:', type: 'longtext', default: "Willkommen bei der\nWissensdrehscheibe für\nbarrierefreie Technologie" },
  ];
}

// Main entry point; here we construct our solid: 
function main(params)
{
	const braillestr = braille_str(params.text.toLowerCase());
	var finalobject = braillestr.csg;
	const width = braillestr.width;
	const height = braillestr.height;
	
	var backplate = new CSG.cube({
		center: [height/2,width/2,-plate_thickness/2],
		radius: [height/2,width/2,plate_thickness/2],
	});
	backplate = backplate.setColor([0.4,0.4,0,0.8]);
	
	//if a backplate is used, we union both together
	//if not, we need to half the braille dots (round spheres)
	if(params.backPlate == true)
	{
		finalobject = finalobject.union(backplate);
		//only if a backplate is used, we should render a support plate
		if(params.supportPlate == true)
		{
			var support = new CSG.cube({
				center: [height-1,5,-10],
				radius: [1,2.5,10],
			});
			support = support.setColor([0.4,0.4,0,0.8]);
			finalobject = finalobject.union(support);
			
			support = new CSG.cube({
				center: [height-1,width-5,-10],
				radius: [1,2.5,10],
			});
			support = support.setColor([0.4,0.4,0,0.8]);
			finalobject = finalobject.union(support);
			
			
		}
	} else {
		finalobject = finalobject.subtract(backplate);
	}
	
	//return CGS object of braille string with eventual plates
	return finalobject;
}


const brailleMapSingleChar = {
	'german': {
		'a': [1,0,0,0,0,0],
		'b': [1,0,1,0,0,0],
		'c': [1,1,0,0,0,0],
		'd': [1,1,0,1,0,0],
		'e': [1,0,0,1,0,0],
		'f': [1,1,1,0,0,0],
		'g': [1,1,1,1,0,0],
		'h': [1,0,1,1,0,0],
		'i': [0,1,1,0,0,0],
		'j': [0,1,1,1,0,0],
		'k': [1,0,0,0,1,0],
		'l': [1,0,1,0,1,0],
		'm': [1,1,0,0,1,0],
		'n': [1,1,0,1,1,0],
		'o': [1,0,0,1,1,0],
		'p': [1,1,1,0,1,0],
		'q': [1,1,1,1,1,0],
		'r': [1,0,1,1,1,0],
		's': [0,1,1,0,1,0],
		't': [0,1,1,1,1,0],
		'u': [1,0,0,0,1,1],
		'v': [1,0,1,0,1,1],
		'w': [0,1,1,1,0,1],
		'x': [1,1,0,0,1,1],
		'y': [1,1,0,1,1,1],
		'z': [1,0,0,1,1,1],
		'ü': [1,0,1,1,0,1],
		'ö': [0,1,1,0,0,1],
		'ä': [0,1,0,1,1,0],
		',': [0,0,1,0,0,0],
		';': [0,0,1,0,1,0],
		':': [0,0,1,1,0,0],
		'.': [0,0,0,0,1,0],
		'!': [0,0,1,1,1,0],
		'(': [0,0,1,1,1,1],
		')': [0,0,1,1,1,1],
		'?': [0,0,1,0,0,1],
		'-': [0,0,0,0,1,1],
		'„': [0,0,1,0,1,1],
		'“': [0,0,0,1,1,1],
		'‘': [0,0,0,0,0,1],
		'‘': [0,0,0,0,0,1],
		'`': [0,0,0,0,0,1],
		'´': [0,0,0,0,0,1],
		' ': [0,0,0,0,0,0]
	}
};

const brailleMapDigits = {
	'german': {
		'start': [0,1,0,1,1,1],
		'1': [1,0,0,0,0,0],
		'2': [1,0,1,0,0,0],
		'3': [1,1,0,0,0,0],
		'4': [1,1,0,1,0,0],
		'5': [1,0,0,1,0,0],
		'6': [1,1,1,0,0,0],
		'7': [1,1,1,1,0,0],
		'8': [1,0,1,1,0,0],
		'9': [0,1,1,0,0,0],
		'0': [0,1,1,1,0,0]
	}
}

const brailleMapDoubleChar = {
	'german': {
		'st': [0,1,1,1,1,1],
		'au': [1,0,0,0,0,1],
		'eu': [1,0,1,0,0,1],
		'ei': [1,1,0,0,0,1],
		'ch': [1,1,0,1,0,1],
		'äu': [0,1,0,0,1,0],
		'ie': [0,1,0,0,1,1]
	}
};

const brailleMapTripleChar = {
	'german': {
		'sch': [1,0,0,1,0,1]
	}
};

/*
const brailleMap = 
[
    //0 -> German Braille
    [
        //structure: [first line left, first line right, second line left, second line right, third line left, third line right]
        //WARNING: if combinations are used (e.g. "sch") these must be located BEFORE any single character it contains!
        ["sch",[1,1,1,1,1,1]],
        ["a",[1,0,0,0,0,0]],
        ["b",[1,0,1,0,0,0]],
        ["c",[1,1,0,0,0,0]],
        ["d",[1,1,0,1,0,0]],
        ["e",[1,0,0,1,0,0]],
        ["f",[1,1,1,0,0,0]],
        ["g",[1,1,1,1,0,0]],
        ["h",[1,0,1,1,0,0]],
        ["i",[0,1,1,0,0,0]],
        ["j",[0,1,1,1,0,0]],
        ["k",[1,0,0,0,1,0]],
        ["l",[1,0,1,0,1,0]],
        ["m",[1,1,0,0,1,0]],
        ["n",[1,1,0,1,1,0]],
        ["o",[1,0,0,1,1,0]],
        ["p",[1,1,1,0,1,0]],
        ["q",[1,1,1,1,1,0]],
        ["r",[1,0,1,1,1,0]],
        ["s",[0,1,1,0,1,0]],
        ["t",[0,1,1,1,1,0]],
        ["u",[1,0,0,0,1,1]],
        ["v",[1,0,1,1,1,0]],
        ["w",[0,1,1,1,0,1]],
        ["x",[1,1,0,0,1,1]],
        ["y",[1,1,0,1,1,1]],
        ["z",[1,0,0,1,1,1]],
        ["ü",[1,0,1,1,0,1]],
        ["ö",[0,1,1,0,0,1]],
        ["ä",[0,1,0,1,1,0]],
        [",",[0,0,1,0,0,0]],
        [";",[0,0,1,0,1,0]],
        [":",[0,0,1,1,0,0]],
        [".",[0,0,0,0,1,0]],
        ["!",[0,0,1,1,1,0]],
        ["(",[0,0,1,1,1,1]],
        [")",[0,0,1,1,1,1]],
        ["?",[0,0,1,0,0,1]],
        ["-",[0,0,0,0,1,1]],
        ["„",[0,0,1,0,1,1]],
        ["“",[0,0,0,1,1,1]],
        ["‘",[0,0,0,0,0,1]],
        ["‘",[0,0,0,0,0,1]],
        ["`",[0,0,0,0,0,1]],
        ["´",[0,0,0,0,0,1]],
        [" ",[0,0,0,0,0,0]]
    ],
    //1 -> unused...
    [
    
    
    ]
];
* */

/*++++ NOTHING TO CONFIGURE FROM HERE ++++*/

//distance between two dots
const spacing = 2.5;
//distance between dot 1 of first character and dot 1 of next character
const distance = 6;
//distance between 2 lines
const plate_height = 10.8;

//how many points in one row (normally fixed, there is no braille standard with more than 2points in one row)
const row_size = 2;
//how many braille dots are used
const bitmap_size = row_size * col_size;


//determine the X location of one dot within a letter
function loc_x(loc) {
	return Math.floor(loc / row_size) * spacing + spacing;
}
//determine the Y location of one dot within a letter
function loc_y(loc) {
	return loc % row_size * spacing  + (distance-spacing)/2;
}

//creates one braille letter.
//parameters:
//bitmap array of all printed dots (e.g. [0,0,1,1,0,0])
function letter(bitmap) {
	var dots = [];
	
	//iterate over all 6 or 8 dots
	for (loc = 0; loc < bitmap_size; loc++) {
		//if the dot is set
		if (bitmap[loc] != 0) {
			//add the sphere CSG object to the array
			dots.push(CSG.sphere({
				center: [loc_x(loc), loc_y(loc), 0],
				radius: diameter/2,
				resolution: resolution,
			}));
		}
	}
	//new CSG object to union all dots
	var csg = new CSG();
	return csg.union(dots);
}

//source:
//https://stackoverflow.com/questions/1098040/checking-if-a-key-exists-in-a-javascript-object
function isKeyInObject(obj, key) {
    return res = Object.keys(obj).some(v => v == key);
}

//find the offset in the braille dots array for a given substring
//this function will determine if the beginning of the given string
//is located in the braille array. There might be a combination of more
//than one character, so we return here:
//[count of "consumed" characters, array of braille dots array]
//parameters: line currently used string
//prev_char previous character
function finddots(line, prev_char) {
	var retval = [0,[]];
	
	//0.) test if previous character was a number
	if(isKeyInObject(brailleMapDigits[brailledialect],prev_char))
	{
		//if yes, push a space character to separate digits/letters
		retval[1].push([0,0,0,0,0,0]);
	}
	
	//1.) detect if we have a 3character braille letter
	if(isKeyInObject(brailleMapTripleChar[brailledialect],line.substr(0,3)))
	{	
		retval[0] = 3;
		retval[1].push(brailleMapTripleChar[brailledialect][line.substr(0,3)]);
		return retval;
	}

	//2.) detect if we have a 2character braille letter
	if(isKeyInObject(brailleMapDoubleChar[brailledialect],line.substr(0,2)))
	{
		retval[0] = 2;
		retval[1].push(brailleMapDoubleChar[brailledialect][line.substr(0,2)]);
		return retval;
	}
	
	//3.) detect if we have a single character braille letter
	if(isKeyInObject(brailleMapSingleChar[brailledialect],line.substr(0,1)))
	{
		retval[0] = 1;
		retval[1].push(brailleMapSingleChar[brailledialect][line.substr(0,1)]);
		return retval;
	}
	
	//4.) detect if we enter the number mode
	if(isKeyInObject(brailleMapDigits[brailledialect],line.substr(0,1)))
	{
		//because we pushed a space character at the beginning for exiting
		//number mode, we need to clear the return array here.
		retval[1] = [];
		
		//we have a digit now...
		//test if previous character was a digit too.
		//if yes, just return the current braille map
		if(isKeyInObject(brailleMapDigits[brailledialect],prev_char))
		{
			retval[0] = 1;
			retval[1].push(brailleMapDigits[brailledialect][line.substr(0,1)]);
		} else {
			//if not, start with the digit start symbol.
			retval[0] = 1;
			retval[1].push(brailleMapDigits[brailledialect]['start']);
			retval[1].push(brailleMapDigits[brailledialect][line.substr(0,1)]);
		}
		return retval;
	}
	
	//if nothing found:
	retval[0] = -1;
	retval[1] = 1;
	return retval;
}


//creates one braille line
//parameters:
//line one text string, which is used to create one line
function braille_line(line) {
	var char_count = 0;
	var braille_count = 0;
	var chararr = [];
	
	do {
		//find all necessary braille characters (dot maps)
		//we need the previous character as well, to detect if we need a
		// number start braille character
		if(char_count != 0) var retval = finddots(line.substr(char_count),line[char_count-1]);
		else var retval = finddots(line.substr(char_count)," ");
		if(retval[0] != -1)
		{
			for(var i = 0; i<retval[1].length; i++) 
			{
				chararr.push(letter(retval[1][i]).translate([0,braille_count*distance,0]))
				braille_count++;
			}
			char_count += retval[0];
		//if no valid character is found, go to next one
		} else char_count++;
	//iterate until each character is done
	} while(char_count < line.length);
	
	console.log("Total Width: " + distance * braille_count + "mm");
	
	CSGLine = new CSG();
	CSGLine = CSGLine.union(chararr);
	return {
		csg: CSGLine,
		width: distance * braille_count,
	};
}

function braille_str(text)
{
	//split the input strings into each line
	var textarr = text.split("\n");
	//array of CSG objects for each line
	var linearr = [];
	var maxwidth = 0;
	
	for(line = 0; line < textarr.length; line++)
	{
		//create one braille line
		var brailleline = braille_line(textarr[line]);
		//save CGS object to array
		linearr.push(brailleline.csg.translate([plate_height * line,0,0]));
		//determine maximum width value
		maxwidth = Math.max(maxwidth,brailleline.width);
	}
	
	var fullstr = new CSG();
	fullstr = fullstr.union(linearr);
	return {
		csg: fullstr,
		width: maxwidth,
		height: plate_height * textarr.length,
	};
}
