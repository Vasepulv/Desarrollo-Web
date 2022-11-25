

function addGraph1(dictResp1){
    var i=0;
    var x=[];
    var y=[];
    if (dictResp1=={}){
        x=0;
    }
    else{
        keys=Object.keys(dictResp1);
        for (key in keys){
            x.push(dictResp1[key]["fecha"]);
            y.push(dictResp1[key]["total"]);
            
        }
        var options = {
            series: {
                lines: { show: true },
                points: { show: true }
            }
        };
        plot1=document.getElementById("plot1");
        Highcharts.chart('plot1',{
            chart: {
                type: 'line'
            },
            title: {
                text: 'Cantidad de eventos por dia.'
            },
            yAxis: {
                title: {
                    text: 'Dias'
                }
            },

            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
        
            xAxis: {
                accessibility: {
                    rangeDescription: 'Cantidad de Eventos'
                },
                categories:x
            },
            series: {
                name:"Eventos por dia",
                data:y
            }
        });
    }

}

function addGraph2(dictResp2){
    var categories=[];
    var data=[];
    if (dictResp2=={}){
        console.log("There is not plot");
    }
    else{
        keys=Object.keys(dictResp2);
        values=Object.values(dictResp2);
        for(key in keys){
            categories.push(dictResp2[key]["tipo"]);
        }
        data.push(values);
        Highcharts.chart('plot2',{
            chart: {
                type: 'pie'
              },
              title: {
                text: "Distribucion de los tipos de comida"
              },
              subtitle: {
                text: null
              },
              series: {
                  name: "Tipos",
                  colorByPoint: true,
                  data: data
              }
        });
    }

}

function addGraph3(dictResp31, dictResp32, dictResp33){
    var x=['January','February','March','April','May','June','July','August','September','October','November','December'];

    var y1=[0,0,0,0,0,0,0,0,0,0,0,0];
    var y2=[0,0,0,0,0,0,0,0,0,0,0,0];
    var y3=[0,0,0,0,0,0,0,0,0,0,0,0];

    if (dictResp31={}){
        console.log("No se pudo graficar debido a que no hay eventos ocurriendo en la mañana");
    }
    else{
        keys=Object.keys(dictResp31);
        var i=0;
        for (key in keys){
            if (dictResp31[key]["mes"] in x){
                y1[i]=dictResp31[key]["total"];
                i++;
            }
        }
        plot31=document.getElementById("plot31");
        p1={data:(x,y1),bars: { show: true }}
        //$.plot(plot31,p1)
    }

    if (dictResp32=={}){
        console.log("No se pudo graficar debido a que no hay eventos ocurriendo en el mediodia");

    }
    else{
        keys=Object.keys(dictResp32);
        var i=0;
        for (key in keys){
            if (dictResp32[key]["mes"] in x){
                y2[i]=dictResp32[key]["total"];
                i++;
            }
        }
        plot32=document.getElementById("plot32");
        p2={data:(x,y2),bars: { show: true }}
        //$.plot(plot32,p2)
    }

    if (dictResp33=={}){
        console.log("No se pudo graficar debido a que no hay eventos ocurriendo en la tarde");
    }
    else{
        keys=Object.keys(dictResp33);
        var i=0;
        for (key in keys){
            if (dictResp33[key]["mes"] in x){
                y3[i]=dictResp33[key]["total"];
                i++;
            }
        }
        plot33=document.getElementById("plot33");
        p3={data:(x,y3),bars: { show: true }}
        //$.plot(plot33,p3)
    }

}



const xhttp=new XMLHttpRequest();

var dictResp1;
var dictResp2;
var dictResp31;
var dictResp32;
var dictResp33;

xhttp.onload=function(){
    dict=xhttp.responseText;
    l=dict.split('\n');
    dictResp1=l[2];
    dictResp2=l[3];
    dictResp31=l[4];
    dictResp32=l[5];
    dictResp33=l[6];

    addGraph1(dictResp1);
    addGraph2(dictResp2);
    addGraph3(dictResp31,dictResp32,dictResp33);
}

xhttp.open("GET","estadisticas.py",true);
xhttp.send();