let menue = document.querySelector(".mobile-navi-icon");
let search = document.querySelector(".mobile-search-icon");
let clc = document.querySelector(".mobile-close");
let links = document.querySelector(".links");

let searchBar = document.querySelector(".search-bar");
menue.addEventListener("click", ()=>{
    links.style.display = "flex";
    menue.style.display = "none";
    search.style.display = "none";
    searchBar.style.display = "none";
    clc.style.display = "flex";
    console.log("meneu")
})

search.addEventListener("click", ()=>{
    links.style.display = "none";
    menue.style.display = "none";
    search.style.display = "none";
    clc.style.display = "flex";
    searchBar.style.display = "block";
    console.log("search")
})


clc.addEventListener("click",()=>{
    clc.style.display = "none";
    searchBar.style.display = "none";
    links.style.display = "none";
    search.style.display = "flex";
    menue.style.display = "flex";
})

let inputSearch = document.querySelector(".search");
let searchResult = document.querySelector(".search-result");
let itmes = document.querySelectorAll(".search-item");

inputSearch.addEventListener("click", ()=>{ 
    if ( searchResult.classList.contains("filter")){
        searchResult.classList.remove("filter")
    }else{
        searchResult.classList.add("filter")
    }
    
})



inputSearch.addEventListener("keyup", (event)=>{
    let input = event.target.value;
    if ( input.length > 2 ){
        for (let i=0; i < itmes.length; i++){
            let row = itmes[i].firstElementChild.children;
            console.log(row[0].innerHTML.indexOf(input));
            console.log(input)
            if (row[0].innerHTML.indexOf(input) < 0 && row[1].innerHTML.indexOf(input) < 0) {
                itmes[i].classList.add("filter")
            }else{
                    itmes[i].classList.remove("filter");
            }
        }
    }else{
        for (let i=0; i < itmes.length; i++){
            itmes[i].classList.remove("filter")
        }
    }
})