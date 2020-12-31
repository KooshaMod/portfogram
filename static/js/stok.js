/// menue select functionality //
console.log("params")
let select = document.querySelector("#select");
let finance = document.querySelector("#finance");
let intro = document.querySelector("#intro");
let Profitability = document.querySelector("#Profitability");
let ratio = document.querySelector("#ratio");
let expand = document.querySelector("#expand");
let raise = document.querySelector("#raise");
let conferance = document.querySelector("#conferance");

select.addEventListener("change", (event)=>{
    finance.style.display = "none";
    intro.style.display = "none";
    Profitability.style.display = "none";
    ratio.style.display = "none";
    expand.style.display = "none";
    raise.style.display = "none";
    conferance.style.display = "none";
    let id = event.target.value;
    let result = document.getElementById(id)
    result.style.display = "flex";
})

class Candel {
    constructor (lowest, heighest, openPrice, closePrice, date, name) {
        this.lowest = lowest;
        this.heighest = heighest;
        this.openPrice = openPrice;
        this.closePrice = closePrice;
        this.date = new Date(date);
        this.name = name;
    }
    getDate(){
        let d = new Date(this.date)
            return d.toLocaleString('default', { year: 'numeric', month: 'long', day: 'numeric' })
    }
    
}


let quaryString = window.location.search;
let urlParams = new URLSearchParams(quaryString);
let s = urlParams.get('stocks');

axios.get("http://127.0.0.1:8000/stocks/api", {
    params : {name : s}
}).then(response=> {
    console.log(response.data)
    let result = JSON.parse(response.data);
    let candles = [];
    for (let r of result){
        console.log(r.name)
        let c = new Candel(r.highest_price, r.lowest_price, r.first_price, r.close_price, r.date, r.name);
        // c.date = c.getDate()
        candles.push(c)
    }
     return candles

}).then(candles=> {
    let name;
    dataPoints = [];
    for (c of candles){
        if (c.date == "Invalid Date"){
            continue
        }else{
        name = c.name;
        dataPoints.push({
            x : c.date,
            y : [
                c.openPrice,
                c.lowest,
                c.heighest,
                c.closePrice,
            ]
        })
    }
    }
    console.log(name, "name")
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        exportEnabled: true,
        title: {
            text: name
        },
        
        axisX: {
            interval: 1,
            valueFormatString: "MMM"
        },
        axisY: {
            includeZero: false,
            prefix: "ریال ",
            title: "قیمت"
        },
        toolTip: {
            content: "Date: {x}<br /><strong>Price:</strong><br />Open: {y[0]}, Close: {y[3]}<br />High: {y[1]}, Low: {y[2]}"
        },
        data: [{
            type: "candlestick",
            yValueFormatString: "$##0.00",
            dataPoints: dataPoints
        }]
    });
    chart.render();
})


    
  



