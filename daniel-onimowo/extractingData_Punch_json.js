//Extracting Data from PunchNg

topStories = document.querySelectorAll('h3');
let response = {};

for (let count = 0; count < topStories.length; count++){
response[count] = topStories[count].textContent;
}

document.write(JSON.stringify(response));

//Output in JSON format

{"0":"ICYMI: I’ve yet to have sex with my sex doll –Pretty Mike","1":"NBA star Steve Curry escapes death in auto crash","2":"Kidnapped Plateau monarch regains freedom","3":"Confederation Cup: Spanish coach Garrido seeks historic title with Raja","4":"May heads to Brussels as Spain threatens Brexit summit","5":"Police arrest two Yahoo boys, security guard over murder of DELSU student","6":"Stray bullet kills trader, injures others in Rivers","7":"Pathetic state of Katsina school where pupils sit on bare floor","8":"Service chiefs have become APC’s lackeys –CSOs","9":"Hijab controversy: UI International School may reopen Monday","10":"Boxing is ruining our sex lives, giving us tears –Nigerian female boxers","11":"Tributes as Credit Switch boss, Bademosi, is buried in Ondo","12":"Falcons battle Equatorial Guinea for AWCON semi-final spot","13":"Three men jailed in Benue for selling neighbour’s son","14":"Customs intercept another 13 containers of Tramadol at Tin Can","15":"Punch Games"}