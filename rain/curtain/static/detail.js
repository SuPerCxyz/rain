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


var pie_tmp = { 
    color: color_list,
    title: {
        left: 'center',
        textStyle: {
            color: '#ccc',
            fontSize: '25',
        },
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        bottom: 0,
        data:['iowait','system','user','idle']
    },
    series : [
        {
            name:'Core usage',
            type:'pie',
            radius : [50, 120],
            center : '50%',
            roseType : 'radareaius',
            label: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            lableLine: {
                normal: {
                    show: false
                },
                emphasis: {
                    show: true
                }
            },
            data:[]
        },
    ]
}


function GetRequest() { 
	var url = location.search;
	var theRequest = new Object(); 
	if (url.indexOf("?") != -1) {
		var str = url.substr(1); 
		strs = str.split("&"); 
		for(var i = 0; i < strs.length; i ++) {
			theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]); 
		} 
	} 
    return theRequest
}

function cpu_detail() {
    var req = GetRequest()
    var nodes = req['nodes']
    var counts = req['count']
    var tmp = {
        color: color_list,
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
            top: '40',
            left: '3%',
            right: '1%',
        },
    }
    var CPU = Object.assign({}, tmp)
    var sys_load = Object.assign({}, tmp)
    var datas = {
        'nodes': nodes,
        'count': counts,
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
                itemGap: 30,
            };
            CPU['xAxis'] = [{
                type: 'category',
                boundaryGap: false,
                data: data.cpu_detail.time,
            }]
            CPU['series'] = cpu_seriess;
            CPU['title'] = {
                text: 'Core usage',
                left: '0',
            }
            var newdiv = document.createElement("cpu");
            newdiv.id='cpu';
            newdiv.style.width="1500px";
            newdiv.style.height="300px";
            newdiv.style.cssFloat="left";
            var dom1 = document.getElementById('cpu_detail').appendChild(newdiv);
            var myChart1 = echarts.init(dom1);
            myChart1.setOption(CPU, true);
    

            var load_1 = data.cpu_detail.system_load.sys_load_1
            var load_5 = data.cpu_detail.system_load.sys_load_5
            var load_15 = data.cpu_detail.system_load.sys_load_15
            var load_series = [
                {
                    name: 'load_1',
                    type: 'line',
                    showSymbol: false,
                    data: load_1,
                    smooth: 0.3,
                },
                {
                    name: 'load_5',
                    type: 'line',
                    showSymbol: false,
                    data: load_5,
                    smooth: 0.3,
                },
                {
                    name: 'load_15',
                    type: 'line',
                    showSymbol: false,
                    data: load_15,
                    smooth: 0.3,
                },
            ]
            sys_load['legend'] = {
                data: ['load_1', 'load_5', 'load_15'],
                bottom: 0,
                itemGap: 30,
            }
            sys_load['series'] = load_series
            sys_load['xAxis'] = [{
                type: 'category',
                boundaryGap: false,
                data: data.cpu_detail.time,
            }]
            sys_load['title'] = {
                text: 'System load',
                left: '0',
            }
            var newdiv2 = document.createElement("sys_load");
            newdiv2.id='sys_load';
            newdiv2.style.width="1500px";
            newdiv2.style.height="300px";
            newdiv2.style.cssFloat="left";
            var dom2 = document.getElementById('cpu_detail').appendChild(newdiv2);
            var myChart2 = echarts.init(dom2);
            myChart2.setOption(sys_load, true);

            var cpu_detail_list = data.cpu_detail.cpu_detail_info
            $.each(cpu_detail_list, function(i, j) {
                var cpu_pie = pie_tmp
                one_result = cpu_detail_list[i]
                cpu_pie.title['text'] = i
                var uasge_data_list = new Array()
                var test = 0
                $.each(j, function(x, y) {
                    var uasge_data_dict = {}
                    uasge_data_dict['name'] = x
                    uasge_data_dict['value'] = y
                    test = test + 1
                    uasge_data_list[test] = uasge_data_dict
                })
                cpu_pie.series[0].data = uasge_data_list
                var piediv = document.createElement('core_usage')
                piediv.id='core_usage'
                piediv.style.width='300px'
                piediv.style.height='350px'
                piediv.style.cssFloat='left'
                var dom = document.getElementById('cpu_detail').appendChild(piediv)
                var myChart = echarts.init(dom)
                myChart.setOption(cpu_pie, true)
            })
        }
    });
}