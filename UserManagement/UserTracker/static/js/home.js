
      function get_graph_data(e){
        // const request=new XMLHttpRequest()
        // document.querySelector("#bargraph24").children[1].value
        console.log(e.target.parentNode.id)

        // const data= new FormData()
        // data.append('starting_date',document.querySelector("#bargraph24").children[1].value)
        // request.send(data)
        data_to_check=e.target.parentNode.children[1].value
        e.target.parentNode.children[1].value=''
        // bar_graph()
        var url_to_hit
        if (e.target.parentNode.id=="bargraph24"){
          url_to_hit="/bargraph/"
        }
        
        console.log(url_to_hit)
        bar_graph(data_to_check,e.target.parentNode,url_to_hit)
      }
      function get_week_month_graph_data(e){
        starting_date=e.target.parentNode.children[1].value
        e.target.parentNode.children[1].value=''
        end_date=e.target.parentNode.children[2].value
        e.target.parentNode.children[2].value=''
        console.log(starting_date)
        const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
        var firstDate = new Date(starting_date);
        var secondDate = new Date(end_date);

        var diffDays = Math.round(Math.abs((firstDate - secondDate) / oneDay))+1;
        console.log(diffDays)
        if (e.target.parentNode.id=="bargraphweek"){
          url_to_hit="/daysbar/"
          if (diffDays != 7){
           alert("Please select a window of 7 days") 
           return null
          }
          
        }
        if (e.target.parentNode.id=="bargraphmonth"){
          url_to_hit="/daysbarweek/"
          if (diffDays != 30){
            alert("Please select a window of 30 days") 
            return null
           }
        }
        graph_week_month(starting_date,end_date,e.target.parentNode,url_to_hit)
      }
      function bar_graph(data,target,url){
      $.ajax({
        url: url,
        type:"POST",
        data: {
          'starting_date':data
        },
        dataType: 'json',
        success: function (data) {
          console.log(data)
          var target_24=target
          target_24.children[3].src=`data:image/png;base64,${data.data}`
         
        }
      });
      }
      function graph_week_month(starting_date,end_date,target,url){
        $.ajax({
          url: url,
          type:"POST",
          data: {
            'starting_date':starting_date,
            "end_date":end_date,
          },
          dataType: 'json',
          success: function (data) {
            console.log(data)
            var target_24=target
            target_24.children[4].src=`data:image/png;base64,${data.data}`
           
          }
        });
        }
      
      function download() {
        let pdf = new jsPDF('l', 'pt', [1920, 640]);
        pdf.html(document.querySelector('#DataTables_Table_0'), {
            callback: function (pdf) {
                pdf.save('test.pdf');
            }
        });
    }
   
       