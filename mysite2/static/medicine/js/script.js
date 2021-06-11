window.addEventListener("load" , function (){

    console.log("hello");


    $("#search_button").on("click", function(){ required_search()  });

});

function required_search(){
    console.log($("#search_text").val());
}

