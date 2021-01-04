function Allow(e){
    var div= e.target.parentNode
    var id= div.dataset.info
    var $this=$(div)
 //    console.log(div)
    $.ajax({
        url:"{% url 'GiveRightsUser' %}",
        type:"POST",
        data:{"profile_id":id},
        context:div,
        dataType:'json',
        success: function(data){
         
         var div=document.querySelector(`[data-info="${data.profile_id}"]`)
         div.remove()
        }
    }) 
 }