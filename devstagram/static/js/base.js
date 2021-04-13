function popUpFunction(el, secEl=undefined) {
    let element = undefined
    switch (el){
        case 'nav':
            targetEl = 'myDropDown'
            element =  document.getElementById('myDropdown')
            break;
        case 'chat':
            element =  document.getElementById('chatdropdown')
            break;
        case 'picSend':
            element =  secEl.get(0)
            break;
    }
    element.classList.toggle("show");
    window.onclick = function(event){

        if ($(event.target).is('.content')){
            if(element.classList.contains("show")) {
                element.classList.toggle("show");
                return
            }
        }
    }
}


function navbarFunction() {
    var x = document.getElementById("navigation");
    if (x.className === "navigation") {
        x.className += " responsive";
    } else {
        x.className = "navigation";
    }
}

// window.onclick = function(event){
//     if ($(event.target).is('.sendpost')){
//         document.getElementById('pic-send-box').toggle("show")
//         console.log('yes')
//     }
// }



// function notificationsFunction() {
//     let element =  document.getElementById("myDropdown")
//     element.classList.toggle("show");
//     window.onclick = function(event){
//         console.log($(event.target))
//         if ($(event.target).is('.content')){
//             if(element.classList.contains("show")) {
//                 element.classList.toggle("show");
//                 return
//             }
//         }
//     }
// }
//
//
// function chatFunc() {
//     let chatBox = document.getElementById("chatdropdown")
//     chatBox.classList.toggle("show");
//     window.onclick = function(event){
//         console.log($(event.target))
//         if ($(event.target).is('.content')){
//             if(chatBox.classList.contains("show")) {
//                 chatBox.classList.toggle("show");
//                 return
//             }
//         }
//     }
// }
//
// function sendPicFunc(){
//     let sendBox = document.getElementById("pic-send-box")
//     sendBox.classList.toggle("show")
//     window.onclick = function(event){
//         console.log($(event.target))
//         if ($(event.target).is('.content')){
//             if(sendBox.classList.contains("show")) {
//                 sendBox.classList.toggle("show");
//                 return
//             }
//         }
//     }
//
// }


// window.onclick = function (event) {
//     if (!event.target.matches('.dropbtn')) {
//         var dropdowns = document.getElementsByClassName("dropdown-content");
//         var i;
//         for (i = 0; i < dropdowns.length; i++) {
//             var openDropdown = dropdowns[i];
//             if (openDropdown.classList.contains('show')) {
//                 openDropdown.classList.remove('show');
//             }
//         }
//     }
// }



function sendPicFunc(){
    document.getElementById("pic-send-box").classList.toggle("show")
}
//
// window.onclick = function (event) {
//     if (!event.target.matches('.pic-send-btn')) {
//         var dropdowns = document.getElementsByClassName("pic-send-box");
//         var j;
//         for (j = 0; j < dropdowns.length; j++) {
//             var openDropdown = dropdowns[j];
//             if (openDropdown.classList.contains('show')) {
//                 openDropdown.classList.remove('show');
//             }
//         }
//     }
// }




