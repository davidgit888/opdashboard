var liNum;
$(function () {
    var h = $(window).height();
    $("#show").css("height", h);
    var listC = "";
    listC = $.ajax({ url: "./TXT/index.txt", async: false, contentType: "application/x-www-form-urlencoded; charset=UTF-8" });
    var lc = listC.responseText.split('\r\n');
    for (var i = 0; i < lc.length; i++) {
        $("#nav").append("<li onclick='cutlist(this)'><a  href='#'>" + lc[i] + "</a></li>");
    };

    liNum = $('#nav').find('li').length;
    //document.write(lc)
    change();

    //显示日期时间
    var t = null;
    t = setTimeout(time, 2000000);//开始执行
    function time() {
        clearTimeout(t);//清除定时器
        var today = new Date();//定义日期对象     
        var yyyy = today.getFullYear();//通过日期对象的getFullYear()方法返回年      
        var MM = today.getMonth() + 1;//通过日期对象的getMonth()方法返回年      
        var dd = today.getDate();//通过日期对象的getDate()方法返回年       
        var hh = today.getHours();//通过日期对象的getHours方法返回小时     
        var mm = today.getMinutes();//通过日期对象的getMinutes方法返回分钟     
        var ss = today.getSeconds();//通过日期对象的getSeconds方法返回秒  
        document.getElementById("time").innerHTML = yyyy + "年" + MM + "月" + dd + "日" + hh + "时" + mm + "分" ;
        //t = setTimeout(time, 2000000); //设定定时器，循环执行            
    }
});

var falg = 0;
var i = 0;
function change() {
    if(falg==0)
    {
        var j = 0;
        $('#nav').find('li').each(function () {
            if (j == i)
            { cutlist(this); }

            j++;
            if (j == liNum)
            { j = 0 }
        })
        i++;
        if (i == liNum)
        { i = 0; }
    }

    //setTimeout("change()", 300000);
}

function changeflag()
{            
    if (falg == 0)
    { setInterval("falg=0;", 100000); }
    falg = 1;
}
function cutlist(lihtml) {
    $("#show").attr("src", lihtml.innerText + ".html");
}