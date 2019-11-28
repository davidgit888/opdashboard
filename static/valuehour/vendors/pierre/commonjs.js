function checkUser(data){
	if(data.user){
	try{
		$('#cost_rate').val(data.user[0].cost_rate);
		$('#quote').val(data.user[0].quote);
		console.log("正在使用外部报价");
		// console.log("费率"+data.user[0].cost_rate);
		$('#original_group').val(data.user[0].original_group);
		$('#work_group').val(data.user[0].work_group);
		if(data.user[0].cost_rate == 0){
			throw "费率设置不完整，无法报工";
		}

	}catch(e){
		layer.msg('你的后台数据配置不完整，请联系管理员:'+e, {icon: 2, time:4000});
		layer.load(2, {shade: [0.1,'#fff']});
	}

	}else{
	layer.msg('你的后台数据配置不完整，请联系管理员!', {icon: 2, time:4000});
	}
}

function reset(){
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getWorkerOpProb/", function(data){
		$("#cost_rate").val(data.user[0].cost_rate);
		$("#quote").val(data.user[0].quote);
	})
	$.ajaxSettings.async = true;
}

function resetInner(){
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getWorkerOpProb/", function(data){
		$("#cost_rate").val(data.user[0].cost_rate);
		$("#quote").val(JSON.parse(data.user[0].flexible).cost);
	})
	$.ajaxSettings.async = true;
}


function checkUser1(data){
	if(data.user){
		try{
			$('#original_group').val(data.user[0].original_group);
			$('#work_group').val(data.user[0].work_group);
			$('#cost_rate').val(data.user[0].cost_rate);
			$('#quote').val(JSON.parse(data.user[0].flexible).cost);
			console.log("正在使用内部报价");
			// console.log("费率"+data.user[0].cost_rate);
			if(data.user[0].cost_rate == 0){
				throw "你的费率设置不完整，无法报工"
			}
		}catch(e){
			layer.msg('你的后台数据配置不完整，请联系管理员:'+e, {icon: 2, time:2000});
			layer.load(2, {shade: [0.1,'#fff']});					
		}
	}else{
		layer.msg('没有读取到你的身份信息，请确认！', {icon: 2, time:2000});
	}
}




function getQueryVariable(variable)
{
	   var query = window.location.search.substring(1);
	   var vars = query.split("&");
	   for (var i=0;i<vars.length;i++) {
			   var pair = vars[i].split("=");
			   if(pair[0] == variable){return pair[1];}
	   }
	   return('');
}

function makep(){
	window.parent.getmachine();
	var index = parent.layer.getFrameIndex(window.name);
	setTimeout(function(){
	  parent.layer.close(index);
	}, 1000);		
}

function get_rest(){
	op = $("#operation").val();
	sfg = $("#sfg").val();
	if (!(op && sfg)){
		$("#restnbr").html('');
		return false;
	}
	var index = layer.load(3, {shade: [0.1,'#fff']});
	$.getJSON('/jzgs/getManHoursSurplus/?sfg='+sfg+'&op='+op, function(data){
		resthour = data;
		if((resthour || resthour == 0) && op!=11){
		$("#restnbr").html('');				
		$("#restnbr").html('(<span class="badge bg-green">剩：'+resthour+'</span>)');				
	}else if(op == 11){
		$("#restnbr").html('');
	};
	});	
	layer.close(index);
};


function get_standard(qty){
	product_type = $("#machine").val();
	op = $("#operation").val();
	prob = $("#prob").val();
	var index = layer.load(3, {shade: [0.1,'#fff']});
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getStandardHours/?product_type="+product_type+"&op="+op+"&prob="+prob, function(data){
		//alert(data.standard);
		standard_hour = data;
		$("#standard_hour").val(Math.round(standard_hour*qty*100)/100);
	});
	$.ajaxSettings.async = true;
	layer.close(index);
};

function get_cat(name){
	$.getJSON("/jzgs/getBorrowType/", function(data){
		target = data['category'];
		result = '';
		$.each(target, function(i, v){
			if(v['a_subject'] == name){
				result = v['a_category'];
			}
		})
		console.log(name);
		return name;
	});
}

function calculate(){
	$("#standard_hour").val("");
	real = $("#real_time").val();
	quote = $("#quote").val();
	cost_rate = $("#cost_rate").val();
	result = real * quote / cost_rate;
	$("#standard_hour").val(result.toFixed(2));
}

function getZaxis(type){
	pattern = /.*\..*\.([0-9][0-9]).*/;
	res = pattern.exec(type);
	return res[1];
}

function getMachineCoeff(product_type){
	//添加机型系数
	type_co = 0;
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getProductCoefficient/", function(data){
		//product_type = $("#machine").val();
		if(product_type.toLowerCase().split(' ')[0]=='global'){
			z_axis = getZaxis(product_type);
			if(parseInt(z_axis)>=12){
				data.forEach(function(item){
					if(item['product'] == 'E/F'){
						type_co = item['para'];
					}
				});
			}else{
				data.forEach(function(item){
					if(item['product'] == 'Global'){
						type_co = item['para'];
					}
				})
			}
		}else{
			for (item in data){
				type  = data[item]['product'];
				if(product_type.toLowerCase().indexOf(type.toLowerCase())!=-1){
					type_co = data[item]['para'];
				}
			}			
		}

	});
	$.ajaxSettings.async = true;
	return type_co;
}

function getOpeYearCoeff(operation = ''){
	//添加工步系数
	operation_co = 0;
	work_year = '';
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getWorkerOpProb/", function(data){
		//operation = $("#operation").val();
		work_year = data.user[0].year;
		//
		if (operation){
			for(item in data['op_list']){
				if(operation == data['op_list'][item]['op_id']){
					operation_co = data['op_list'][item]['coefficient'];
				}
			}			
		}
		//				
	});
	$.ajaxSettings.async = true;
	return [operation_co, getYearCoeff(work_year)];
}

function getYearCoeff(year){
	//添加工龄系数	
	year_co = 0;
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getAgeCoefficient/",function(data){
		for(item in data){
			if(year == data[item]['age']){
				year_co = data[item]['para'];
			}else{
				throw '工龄设置有问题，请联系管理员';
			}
		}
	});
	$.ajaxSettings.async = true;
	return year_co;
}

function getBssoCoeff(type){
	var coeff;
	$.ajaxSettings.async = false;
	$.getJSON("/jzgs/getOpCoefficient/?type="+type,function(data){
		coeff = data;
	})
	$.ajaxSettings.async = true;
	return coeff;
}