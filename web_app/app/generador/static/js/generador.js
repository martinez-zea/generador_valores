function getHistoricalHour(){
	//colors 
	var orange = '#F5631C';
	var yellow = '#F6D10B';
	var pink = '#FB2E80';

	//arrays for historical data
	var valor_60 = [];
	var capital_60 = [];

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
		$('#valor_60').sparkline(valor_60.reverse(),{
			type: 'line',
			width: '470px',
			height: '60px',
			lineColor: orange,
			fillColor: 'transparent',
			spotColor: pink,
			spotRadius: '2',
		});
		$('#capital_60').sparkline(capital_60.reverse(),{
			type: 'line',
			width: '470px',
			height: '60px',
			lineColor: yellow,
			fillColor: 'transparent',
			spotColor: pink,
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
        $('#valor_day_graph').sparkline(val,{
                    type: 'line',
                    width: '390px',
                    height: '50px',
                    lineColor: orange,
                    fillColor: 'transparent',
                    spotColor: pink,
                    spotRadius: '2',
        });
        $('#capital_day_graph').sparkline(cap,{
                    type: 'line',
                    width: '390px',
                    height: '50px',
                    lineColor: yellow,
                    fillColor: 'transparent',
                    spotColor: pink,
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
            console.log('el get esta hecho, tengo respuesta');
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

    function updateWeekChart(cap,val){
        $('#valor_week_graph').sparkline(val,{
            type: 'line',
            width: '390px',
            height: '50px',
            lineColor: orange,
            fillColor: 'transparent',
            spotColor: pink,
            spotRadius: '2',
        });
        $('#capital_week_graph').sparkline(cap,{
            type: 'line',
            width: '390px',
            height: '50px',
            lineColor: yellow,
            fillColor: 'transparent',
            spotColor: pink,
        });
    }

    function updateMonthChart(cap,val){
        $('#valor_month_graph').sparkline(val,{
            type: 'line',
            width: '920px',
            height: '80px',
            lineColor: orange,
            fillColor: 'transparent',
            spotColor: pink,
            spotRadius: '2',
        });
        $('#capital_month_graph').sparkline(cap,{
            type: 'line',
            width: '920px',
            height: '80px',
            lineColor: yellow,
            fillColor: 'transparent',
            spotColor: pink,
        });
    }
   
    for (var i = 0; i <= num_days; i++){    
        getDayLastEvent(initial_day.clone().add('days',i), initial_day.clone().add('days', i+1), function(data){
            cap.push(data.capital);
            val.push(data.valor_unitario);
            if(period === 'week'){
                updateWeekChart(cap,val);
            } else if (period === 'month'){
                updateMonthChart(cap,val);
            }
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

$(document).ready(function(){
    var orange = '#F5631C';
	var yellow = '#F6D10B';
	var pink = '#FB2E80';

    (function updateHour(){
        setTimeout(function(){
            getHistoricalHour();
            updateHour();
        },10000);
    })(); 
    
    (function updateDay(){
        setTimeout(function(){
            getHistoricalDay(moment(),8);
            updateDay();
        },15000);
    })(); 

    (function updateWeek(){
        setTimeout(function(){
            getHistoricalDates(moment(), 5, 'week');
            updateWeek();
        }, 18000);
    })();

    (function updateMonth(){
        setTimeout(function(){
            getHistoricalDates(moment(), 30, 'month');
            updateMonth();
        }, 30000);
    })();
});
