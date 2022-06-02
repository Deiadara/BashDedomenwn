$(document).ready(function(){
    $(document.body).on("click", "td[data-href]", function(){
        window.location.href = this.dataset.href;
    });
});

$(function() {

    var $contextMenu = $("#contextMenu");

    $("body").on("contextmenu", "table tbody tr", function(e) {
         $contextMenu.css({
              display: "block",
              left: e.pageX,
              top: e.pageY
         });
        debugger;
         return false;
    });

    $('html').click(function() {
         $contextMenu.hide();
    });
  
  $("#contextMenu li a").click(function(e){
    var  f = $(this);
    debugger;
  });

});