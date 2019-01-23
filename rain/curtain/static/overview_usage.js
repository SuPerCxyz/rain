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

function get_node_list() {
    $.ajax({
        type: "GET",
        url: "/node_list",
        data: null,
        dataType : "json",
        success: function(result) {
            return result
        }
    });
}

function test(node, id) {
    var dom = document.getElementById(id);
    var myChart = echarts.init(dom);
    def_option(node, myChart)
}

function def_option(node, myChart) {
    var option = {}
    option = {
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
    var datas = {}
    datas ={
        'nodes': node,
        'count': 200
    }
    $.ajax({
        type: "POST",
        url: "/overview",
        data: JSON.stringify(datas),
        dataType : "json",
        success: function(result) {
            for (i = 0, max = result.time_list.length; i < max; i++) {
            option.xAxis[0].data.push(result.time_list[i]);
            option.series[0].data.push(parseFloat(result.cpu_list[i])); 
            option.series[1].data.push(parseFloat(result.mem_list[i])); 
        };
            if (option && typeof option === "object") {
                myChart.setOption(option, true);
            }
        }
    });
}
