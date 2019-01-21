var m = 100
var n = 3

function randomFiveDiffNum(m, n) {
    function sortNumber(a, b){
        return a - b
    }
    var num = [];
    for(var i=0; i<n; i++){
        num[i] = Math.floor(Math.random() * m);
        for(var j=0; j<i; j++){
            if(num[i] == num[j]){
                i--;
            }
        }
    }
    return num.sort(sortNumber);
}

function ls(n) {
    var myDate = new Date();
    myDate.setDate(myDate.getDate() - n);
    var dateArray = []; 
    var dateTemp; 
    var flag = 1; 
    for (var i=0; i<n; i++) {
        dateTemp = (myDate.getMonth() + 1) + "-" + myDate.getDate();
        dateArray.push(dateTemp);
        myDate.setDate(myDate.getDate() + flag);
    }
    return dateArray
}

function def_option(node) {
    var options = {
        title: {
            text: node,
            left: '0',
        },
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            // data: ['cpu', 'memcache', 'network', 'disk'],
            data: ['cpu', 'memcache'],
            bottom: 15,
        },
        xAxis: [
            {
                type: 'category',
                boundaryGap: false,
                data: [],
            }
        ],
        yAxis: [
            {
                type: 'value',  
                axisLabel: {  
                    show: true,  
                    interval: 'auto',  
                    formatter: '{value} %'
                },
                show: true,
            }
        ],
        series: [
            {
                name: 'cpu',
                type: 'line',
                showSymbol: false,
                data: [],
                color: '#89cbf4',
                smooth: 0.3,
            },
            {
                name: 'memcache',
                type: 'line',
                showSymbol: false,
                data: [],
                color: '#F75C2F',
                smooth: 0.3,
            },
            // {
            //     name: 'network',
            //     type: 'line',
            //     showSymbol: false,
            //     data: randomFiveDiffNum(m,n),
            //     color: '#00AA90',
            //     smooth: 0.3,
            // },
            // {
            //     name: 'disk',
            //     type: 'line',
            //     showSymbol: false,
            //     data: randomFiveDiffNum(m,n),
            //     color: '#B481BB',
            //     smooth: 0.3,
            // }
        ]
    }
    return options
}
