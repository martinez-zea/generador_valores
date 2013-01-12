var counter = 0;

function max() {
  if (arguments.length === 2) {
    return arguments[0] < arguments[1] ? arguments[1] : arguments[0];
  }
  var numbers = arguments.length === 1 ? arguments[0] : arguments; // if single argument, array is used
  if (! ("length" in numbers && numbers.length > 0)) {
    throw "Non-empty array is expected";
  }
  var max = numbers[0],
  count = numbers.length;
  for (var i = 1; i < count; ++i) {
    if (max < numbers[i]) {
     max = numbers[i];
    }
  }
  return max;
};

function min() {
  if (arguments.length === 2) {
    return arguments[0] < arguments[1] ? arguments[0] : arguments[1];
  }
  var numbers = arguments.length === 1 ? arguments[0] : arguments; // if single argument, array is used
  if (! ("length" in numbers && numbers.length > 0)) {
    throw "Non-empty array is expected";
  }
  var min = numbers[0],
  count = numbers.length;
  for (var i = 1; i < count; ++i) {
    if (min > numbers[i]) {
      min = numbers[i];
    }
  }
  return min;
};

function norm(aNumber, low, high) {
  return (aNumber - low) / (high - low);
};

function map(value, istart, istop, ostart, ostop) {
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart));
};

function getHistoricalHour(){
	//colors 
	var orange = '#F5631C';
	var yellow = '#F6D10B';
	var pink = '#FB2E80';

	//arrays for historical data
	var valor_60 = [];
    var valor_norm = [];
	var capital_60 = [];
    var capital_norm = [];

	$.get(ESTADO_API, function(data){	
		m = data.objects[0];
        tmp_ = m.timestamp.split('T');
        hr_ = tmp_[1].split('.');

		m.timestamp = tmp_[0] + ',  ' + hr_[0];

		var minute = ich.actual_state(m);
		$('#actual_state').html(minute);
		
		$.each(data.objects, function(key, value){
			valor_60.push(value.valor_unitario);
			capital_60.push(value.capital);
		});
 
    var mini = min(valor_60);
    var maxi = max(valor_60);
    var cmini = min(capital_60);
    var cmaxi = max(capital_60);

    //console.log('mini: ', mini);
    //console.log('maxi: ', maxi);

    for(var i=0; i<valor_60.length; i++){
      valor_norm.push(norm(valor_60[i],mini,maxi));
    }
    for(var i=0; i<capital_60.length; i++){
        capital_norm.push(norm(capital_60[i],cmini,cmaxi));
    }

    //console.log(valor_norm);

		$('#valor_60').sparkline(valor_norm.reverse(),{
		  type: 'line',
			width: '470px',
			height: '40px',
			lineColor: orange,
			fillColor: 'transparent',
			spotColor: pink,
			spotRadius: '2',
            defaultPixelsPerValue: 7,
            chartRangeMin: 0,
            chartRangeMax: 1,
            lineWidth: 2,
		});
		$('#capital_60').sparkline(capital_norm.reverse(),{
			type: 'line',
			width: '470px',
			height: '40px',
			lineColor: yellow,
			fillColor: 'transparent',
			spotColor: pink,
             defaultPixelsPerValue: 7,
            chartRangeMin: 0,
            chartRangeMax: 1,
            lineWidth: 2,
		});
	});
}

function getHistoricalDay(date,numHours){
	//retorna el estado del numero de horas entregado en el
	//parametro numHours
	//colors 
    var	orange = '#F5631C';
	var yellow = '#F6D10B';
	var pink = '#FB2E80';

	var cap = [];
	var val = [];
	var final_hour = date.hours();
	var initial_hour = date.clone().subtract('hours', numHours);

    function updateChart(cap,val){
        var v_norm =[];
        var c_norm = [];

        var vmin = min(val);
        var vmax = max(val);
        var cmin = min(cap);
        var cmax = max(cap);
        
        for (var i = 0; i<val.length; i++){
            v_norm.push(norm(val[i],vmin,vmax));
        }
        for (var i= 0; i<cap.length; i++){
            c_norm.push(norm(cap[i],cmin,cmax));
        }
        
        var period = {periodo: 'dia'}
        var p = ich.day_state(period);
		$('#day_state').html(p);

        $('#valor_week_graph').sparkline(v_norm,{
            type: 'line',
            width: '750px',
            height: '50px',
            lineColor: orange,
            fillColor: 'transparent',
            spotColor: pink,
            spotRadius: '2',
            defaultPixelsPerValue: 7,
            chartRangeMin: 0,
            chartRangeMax: 1,
            lineWidth: 2,
        });
        $('#capital_week_graph').sparkline(c_norm,{
            type: 'line',
            width: '750px',
            height: '50px',
            lineColor: yellow,
            fillColor: 'transparent',
            spotColor: pink,
            spotRadius: '2',
            defaultPixelsPerValue: 7,
            chartRangeMin: 0,
            chartRangeMax: 1,
            lineWidth: 2,
        });
    }
    
	for (var i = 0; i <= numHours; i++){
		getHourLastEvent(initial_hour.clone().add('hours', i), initial_hour.clone().add('hours', i+1), function(data){
			cap.push(data.capital);
			val.push(data.valor_unitario);
			updateChart(cap,val);
		});
	}
	
	function getHourLastEvent(initial, final, cback){
		//pregunta al api y retorna el ultimo objeto encontrado en el rango
		//de la hora 
		
		function formatDate(date){
			//formatea el Date para que respete las necesidades del api
			var formated = date.format('YYYY-MM-DD HH:mm'); 
			return formated;
		}
		
		//construye la url, hace el get y retorna el resultado
		var url = ESTADO_API+'?timestamp__gt='+formatDate(initial)+'&timestamp__lt='+formatDate(final)+'&limit=1';
		$.get(url, function(data){
            //console.log('el get esta hecho, tengo respuesta');
			if(data.meta.total_count > 0){       
				cback(data.objects[0]);
			}
		});
	}

}

function getHistoricalDates(date, num_days, period){
    //retorna los valores para la hora durante el numero de dias especificado
    //en el parametro num_days
    var	orange = '#F5631C';
	var yellow = '#F6D10B';
	var pink = '#FB2E80';

    var cap = [];
    var val = [];
    var initial_day = date.clone().subtract('days', num_days);

    function updateWeekChart(cap,val,period){
        var v_norm =[];
        var c_norm = [];

        var vmin = min(val);
        var vmax = max(val);
        var cmin = min(cap);
        var cmax = max(cap);
        
        for (var i = 0; i<val.length; i++){
            v_norm.push(norm(val[i],vmin,vmax));
        }
        for (var i= 0; i<cap.length; i++){
            c_norm.push(norm(cap[i],cmin,cmax));
        }
        
        if (period ==='week'){
            var period = {periodo: 'semana'}
        }
        if (period === 'month'){
            var period = {periodo: 'mes'}
        }
        var p = ich.day_state(period);
		$('#day_state').html(p);

        $('#valor_week_graph').sparkline(v_norm,{
            type: 'line',
            width: '750px',
            height: '50px',
            lineColor: orange,
            fillColor: 'transparent',
            spotColor: pink,
            spotRadius: '2',
            defaultPixelsPerValue: 7,
            chartRangeMin: 0,
            chartRangeMax: 1,
            lineWidth: 2,
        });
        $('#capital_week_graph').sparkline(c_norm,{
            type: 'line',
            width: '750px',
            height: '50px',
            lineColor: yellow,
            fillColor: 'transparent',
            spotColor: pink,
            spotRadius: '2',
            defaultPixelsPerValue: 7,
            chartRangeMin: 0,
            chartRangeMax: 1,
            lineWidth: 2,
        });
    }

   
    for (var i = 0; i <= num_days; i++){    
        getDayLastEvent(initial_day.clone().add('days',i), initial_day.clone().add('days', i+1), function(data){
            cap.push(data.capital);
            val.push(data.valor_unitario);
            updateWeekChart(cap,val,period);
        }); 
    }
    
    function getDayLastEvent(initial, final, cback){
        //pregunta al api y retorna el ultimo objeto encontrado en el rango
        //de la hora 
        
        function formatDate(date){
            //formatea el Date para que respete las necesidades del api
            var formated = date.format('YYYY-MM-DD HH:mm');  
            return formated;
        }
        
        //construye la url, hace el get y retorna el resultado
        var url = ESTADO_API+'?timestamp__gt='+formatDate(initial)+'&timestamp__lt='+formatDate(final)+'&limit=1';
        $.get(url, function(data){
            if(data.meta.total_count > 0){       
                cback(data.objects[0]);
            }
        });
    }
}



function updateChart(){
    counter++;
    //counter = 4;
    //console.log(counter);
    if(counter === 1){
      $('#day_state').hide();
      $('#actual_state').show();
       getHistoricalHour();
    }
    if(counter === 2){
      $('#actual_state').hide();

      $('#day_state').show();
      getHistoricalDay(moment(),8);
    }
    if(counter === 3){
      $('#actual_state').hide();

      $('#day_state').show();
      getHistoricalDates(moment(), 5, 'week');
    }
    if(counter === 4){
      $('#actual_state').hide();
      //$('#day_state').hide();

      $('#day_state').show();
      getHistoricalDates(moment(), 30, 'month');
      counter = 0;
    }
}

$(window).load(function() {
    $('#actual_state').show();
    $('#day_state').hide();
    $('#capital_month').hide();
    getHistoricalHour();

    $('#info_images').orbit({
        animationSpeed: 800,
        advanceSpeed: 10000,
        directionalNav: false,
        captions: false,
        afterSlideChange: function(){
            updateChart();
        },
    }); 
});

