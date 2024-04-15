function sleep(ms) 
{
    return new Promise(resolve => setTimeout(resolve, ms));
}



// Get the button element
const goToComposebutton = document.querySelector('#composeButton');
const goToInboxbutton = document.querySelector('#inboxButton');
const composeBackBtn = document.querySelector('#composeBack-btn');
const inboxBackBtn = document.querySelector('#inboxBack-btn');

// Get the element you want to change the display of
const underneth = document.querySelector('#unserneth');

const composeScreen = document.querySelector('#composeScreen');

const inboxScreen = document.querySelector('#inboxScreen');

// Add a click event listener to the button
goToComposebutton.addEventListener('click', () => {
    // Change the display of the element to "block"
    underneth.style.animation =  "hide-out 1.5s ease"
    // underneth.style.visibility = "hidden";

    sleep(1100).then(() => { 
        composeScreen.style.visibility = "visible"
        composeScreen.style.position = "relative"
        composeScreen.style.animation =  "show-up 2s ease"
    });
});


// goToInboxbutton.addEventListener('click', () => {
//     // Change the display of the element to "block"
//     underneth.style.animation =  "hide-out 1.5s ease"
//     // underneth.style.visibility = "hidden";
//
//     sleep(1100).then(() => {
//         inboxScreen.style.visibility = "visible"
//         inboxScreen.style.position = "relative"
//         inboxScreen.style.animation =  "show-up 2s ease"
//     });
// });

composeBackBtn.addEventListener('click',() => {
    composeScreen.style.animation =  "hide-out 2s ease"
    sleep(1200).then(() => { 
        composeScreen.style.visibility = "hidden"
        composeScreen.style.position = "inherit"
        underneth.style.animation =  "show-up 1.5s ease"
    });
});

inboxBackBtn.addEventListener('click',() => {
    inboxScreen.style.animation =  "hide-out 2s ease"
    sleep(1200).then(() => { 
        inboxScreen.style.visibility = "hidden"
        inboxScreen.style.position = "inherit"
        underneth.style.animation =  "show-up 1.5s ease"
    });
});


