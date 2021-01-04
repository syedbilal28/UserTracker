
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
        if (e.target.parentNode.id=="bargraphweek"){
          url_to_hit="/daysbar/"
        }
        if (e.target.parentNode.id=="bargraphmonth"){
          url_to_hit="/daysbarweek/"
        }
        console.log(url_to_hit)
        bar_graph(data_to_check,e.target.parentNode,url_to_hit)
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
      
      function download() {
        let pdf = new jsPDF('l', 'pt', [1920, 640]);
        pdf.html(document.querySelector('#DataTables_Table_0'), {
            callback: function (pdf) {
                pdf.save('test.pdf');
            }
        });
    }
   
       