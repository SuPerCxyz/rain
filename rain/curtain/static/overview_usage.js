var m = 100
var n = 3

var color_list = [
    "#2ec7c9",
    "#b6a2de",
    "#5ab1ef",
    "#ffb980",
    "#d87a80",
    "#8d98b3",
    "#e5cf0d",
    "#97b552",
    "#95706d",
    "#dc69aa",
    "#07a2a4",
    "#9a7fd1",
    "#588dd5",
    "#f5994e",
    "#c05050",
    "#59678c",
    "#c9ab00",
    "#7eb00a",
    "#6f5553",
    "#c14089"
]

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


function def_option(node, myChart) {
    var option = {}
    option = {
        color: color_list,
        title: {
            text: node,
            left: '0',
            link:"https://github.com/SuPerCxyz/rain",
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
                smooth: 0.3,
            },
            {
                name: 'memcache',
                type: 'line',
                showSymbol: false,
                data: [],
                smooth: 0.3,
            },
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


function overview() {
    $.ajax({
        type:"GET",
        url:"/node_list",
        dataType: "json",  
        success: function(data){
            $.each(data.node_lists, function(i, j) {
                var newdiv = document.createElement("div");
                newdiv.id=j;
                // newdiv.innerText=j;
                newdiv.style.width="500px";
                newdiv.style.height="300px";
                newdiv.style.cssFloat="left";
                document.getElementById("overviews").appendChild(newdiv);
                var dom = document.getElementById(j);
                var myChart = echarts.init(dom);
                def_option(j, myChart);
            })
        }
    }); 
}


function node_status() {
    $.ajax({
        type:"GET",
        url:"/node_status",
        dataType: "json",  
        success: function(data){
            $.each(data.nodes_status, function(i, j) {
                var newdiv = document.createElement("div");
                newdiv.id=j.time;
                newdiv.style.width="500px";
                newdiv.style.height="40px";
                newdiv.style.cssFloat="left";
                document.getElementById("status").appendChild(newdiv);
                var img = document.createElement("img");
                img.width="23";
                img.style.verticalAlign="middle";
                if (j.status=='Online') {
                    img.src="/static/images/poweron.png";
                }
                else {
                    img.src="/static/images/poweroff.png";
                }
                newdiv.append(img);
                var span = document.createElement("span");
                span.style.fontFamily="Arial, Helvetica, sans-serif";
                span.style.fontSize="25px";
                span.style.verticalAlign="middle";
                span.style.whiteSpace="pre-wrap";
                span.innerText='  ' + j.hostname + '_' + j.ip_address;
                newdiv.append(span);
                // var span1 = document.createElement("span");
                // span1.style.fontFamily="font-family:Arial, Helvetica, sans-serif";
                // span1.style.fontSize="20px";
                // span1.style.verticalAlign="middle";
                // span1.style.whiteSpace="pre-wrap";
                // span1.style.display="block";
                // var cpu_count=j.system_info.cpu.cpu_count
                // var cpu_percent=j.system_info.cpu.cpu_percent
                // var load=j.system_info.cpu.load_1
                // span1.innerText='CPU  count:' + cpu_count + ', percent:' + cpu_percent + ', system load:' + load;
                // newdiv.append(span1);
            })
        }
    }); 
}

function cpu_detail() {
    var CPU = {
        color: color_list,
        // title: {
        //     text: 'acer_121.237.51.0',
        //     left: '0',
        // },
        tooltip: {
            trigger: 'axis',
        },
        yAxis: [
            {
                type: 'value',  
                axisLabel: {  
                    show: true,  
                    interval: 'auto',  
                    formatter: '{value} %',
                },
                show: true,
            }
        ],
        grid: {
            top: '10',
            left: '3%',
            right: '1%',
        },
    }
    var datas = {
        'nodes': 'acer_121.237.51.0',
        'count': 50
    }
    var cpu_seriess = new Array()
    var count = 0
    var legend_list = new Array()
    $.ajax({
        type:"POST",
        url:"/cpu_detail",
        data: JSON.stringify(datas),
        dataType: "json", 
        success: function(data){
            $.each(data.cpu_detail.cpu_info, function(i, j) {
                legend_list[count] = i;
                var cpu_series = {
                    name: i,
                    type: 'line',
                    showSymbol: false,
                    data: j,
                    smooth: 0.3,
                };
                cpu_seriess[count] = cpu_series;
                count += 1;
            });
            CPU['legend'] = {
                data: legend_list,
                bottom: 0,
            };
            var x = [{
                type: 'category',
                boundaryGap: false,
                data: data.cpu_detail.time,
            }]
            CPU['xAxis'] = x
            CPU['series'] = cpu_seriess;
            console.log(CPU['series'])
            var newdiv = document.createElement("cpu");
            newdiv.id='cpu';
            newdiv.style.width="1500px";
            newdiv.style.height="300px";
            newdiv.style.cssFloat="left";
            var dom1 = document.getElementById('cpu_detail').appendChild(newdiv);
            var myChart = echarts.init(dom1);
            myChart.setOption(CPU, true);
        }
    });
}