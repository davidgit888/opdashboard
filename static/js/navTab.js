
function swithTab(){
	//Show and hide li 
        var allLi = $('#navTabContainer').children("li");
        //var today = '{{p_date}}';
        //var p_date = document.getElementById('p_perform_today');
        //var p_date='{{p_date}}';       
        //alert(p_date);
        var allDiv = $('#bodyContainer').children("div")
        for(i=0;i<allLi.length;i++){
            allLi[i].index = i;
            allLi[i].onclick = function (){
                //allLi[i].style.background='#6AC1F7';
                
                for(i=0;i<allLi.length;i++){
                    allLi[i].style.background='#6AC1F7';
                    allDiv[i].style.display='none';
                }
                
                this.style.background='orange';
                allDiv[this.index].style.display='block';
                
                
            //alert(allLi.length);
            //alert(allDiv.length);
                
            //li.style.background='orange';
            //li.style.display='block';
            
            }
        }
}