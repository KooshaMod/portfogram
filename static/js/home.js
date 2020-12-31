// navigation script //

let nav = document.querySelector(".nav-links");
let meneu = document.querySelector(".menue");
let close = document.querySelector(".close");
let clc = document.querySelector(".close-search")
let search = document.querySelector(".search-bar");
let s = document.getElementById("search")
meneu.addEventListener("click", (event)=>{
   nav.style.display = "flex"
})
s.addEventListener("click", (event)=>{
    search.style.display = "flex";
})
close.addEventListener("click",(event)=>{
    nav.style.display = "none";
  
})
clc.addEventListener("click", (event)=>{
    search.style.display = "none";
})


//search in mobile functionality //
let searchResult = document.querySelector(".search-result");
let mobileSearch = document.getElementById("moblie-search");
let items = document.querySelectorAll(".search-item");
console.log(items)
mobileSearch.addEventListener("click", (event)=>{
    searchResult.style.display = "flex";
})
mobileSearch.addEventListener("keyup", (event)=>{
    let input = event.target.value;
    if (input.length > 2){
        for (let i=0; i < items.length; i++){
            let row = items[i].children;
            if ( row[0].innerHTML.indexOf(input) < 0 && row[1].innerHTML.indexOf(input) < 0){
                items[i].classList.add("filter");
            }else{
                items[i].classList.remove("filter");
            }
        }
    }else{
        for (let i=0; i < items.length; i++){
            items[i].classList.remove("filter")
        }
    }
    
})
//select functionality ends here //
