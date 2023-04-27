"use strict";

console.log("aaaaaaaaa");

$(document).on("click", "table tr:not(:first-child) td", (evt) => {
    console.log(evt.target);
});


// $(document).ready(
//     () => {
//         validate_all();
//     }
// );