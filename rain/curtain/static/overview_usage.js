var m = 100
var n = 3


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