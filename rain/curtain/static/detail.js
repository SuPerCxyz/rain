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


function sysoverview() {
    var req = GetRequest()
    var nodes = req['nodes']
    var datas = {
        'nodes': nodes
    }
    $.ajax({
        type:"POST",
        url:"/sysoverview",
        data: JSON.stringify(datas),
        dataType: "json", 
        success: function(data) {
            var a1=document.createElement("table")
            a1.style.letterSpacing='2px'
            a1.style.fontFamily='Arial, Helvetica, sans-serif'
            a1.style.fontSize='20px'
            a1.style.overflow='hidden'
            a1.style.tableLayout='fixed'
            a1.style.wordBreak='break-all'
            a1.style.width='1500px'
            a1.style.border='0'
            var b1=document.createElement("tr")
            var b2=document.createElement("tr")
            var b3=document.createElement("tr")
            var b4=document.createElement("tr")
            a1.appendChild(b1)
            a1.appendChild(b2)
            a1.appendChild(b3)
            a1.appendChild(b4)
            var c1=document.createElement("td")
            var c2=document.createElement("td")
            c1.style.width='50%'
            c2.style.width='50%'
            b1.appendChild(c1)
            b1.appendChild(c2)
            var c3=document.createElement("td")
            var c4=document.createElement("td")
            c3.style.width='50%'
            c4.style.width='50%'
            b2.appendChild(c3)
            b2.appendChild(c4)
            var c5=document.createElement("td")
            var c6=document.createElement("td")
            c6.style.width='50%'
            c5.style.width='50%'
            b3.appendChild(c5)
            b3.appendChild(c6)
            var c7=document.createElement("td")
            c7.style.width='100%'
            c7.colSpan='2'
            b4.appendChild(c7)
            c1.append('Hostname: ' + data.sys_info.hostname)
            c2.append('IP: ' + data.sys_info.ip_address)
            c3.append('Status: ' + data.sys_info.status)
            c4.append('Online user count: ' + data.sys_info.user_count)
            c5.append('Now time: ' + data.sys_info.time)
            c6.append('Boot time: ' + data.sys_info.boot_time)
            c7.append('Kernel info: ' + data.sys_info.system_info)
            document.getElementById('sysoverview1').appendChild(a1)
        }
    })
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
            left: '50',
            right: '30',
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
            newdiv.style.width="750px";
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
            newdiv2.style.width="750px";
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
                piediv.style.width='375px'
                piediv.style.height='350px'
                piediv.style.cssFloat='left'
                var dom = document.getElementById('cpu_detail').appendChild(piediv)
                var myChart = echarts.init(dom)
                myChart.setOption(cpu_pie, true)
            })
        }
    });
}


function mem_detail() {
    var req = GetRequest()
    var nodes = req['nodes']
    var counts = req['count']
    var datas = {
        'nodes': nodes,
        'count': counts,
    }
    $.ajax({
        type:"POST",
        url:"/mem_deatil",
        data: JSON.stringify(datas),
        dataType: "json", 
        success: function(data) {
            var mem_total = data.mem_info.memcache_total_MB
            var mem_avail = data.mem_info.memcache_available_MB
            var mem_used = data.mem_info.memcache_used_MB
            var mem_line = {
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
                    top: '80',
                    left: '50',
                    right: '1%',
                },
            }
            mem_line['series'] = [
                {
                    name: 'memcache used',
                    type: 'line',
                    showSymbol: false,
                    data: data.mem_info.mem_used,
                    smooth: 0.3,
                },
                {
                    name: 'memcache cache and buff',
                    type: 'line',
                    showSymbol: false,
                    data: data.mem_info.mem_bc,
                    smooth: 0.3,
                },
            ]
            mem_line['legend'] = {
                data: ['memcache used', 'memcache cache and buff'],
                bottom: 0,
                itemGap: 30,
            }
            mem_line['xAxis'] = [{
                type: 'category',
                boundaryGap: false,
                data: data.mem_info.time,
            }]
            mem_line['title'] = {
                text: 'Memcache usage',
                left: '0',
                subtext: 'Total: ' + mem_total + '(MB) Used: ' + mem_used + '(MB) Available: ' + mem_avail + '(MB).'
            }
            var newdiv1 = document.createElement("mem")
            newdiv1.id='mem'
            newdiv1.style.width="1100px"
            newdiv1.style.height="400px"
            newdiv1.style.cssFloat="left"
            var dom1 = document.getElementById('mem_detail').appendChild(newdiv1);
            var myChart1 = echarts.init(dom1);
            myChart1.setOption(mem_line, true);


            var mem_pie = {
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
                    data:['used', 'available', 'cache buff']
                },
                series : [
                    {
                        name:'Memcache usage',
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
                        data:[
                            {name: 'used', value: mem_used},
                            {name: 'available', value: mem_avail},
                            {name: 'cache buff', value: mem_total - mem_avail - mem_used}
                        ]
                    },
                ]
            }
            var newdiv2 = document.createElement("mem_pie")
            newdiv2.id='mem_pie'
            newdiv2.style.width="400px"
            newdiv2.style.height="400px"
            newdiv2.style.cssFloat="left"
            var dom2 = document.getElementById('mem_detail').appendChild(newdiv2);
            var myChart2 = echarts.init(dom2);
            myChart2.setOption(mem_pie, true);
        }
    })
}