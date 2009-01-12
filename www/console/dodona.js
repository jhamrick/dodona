$(function onready(){
$('#sendbutton').click(function(){
var input = $('#chatinput').val();
$.get('handler.php?msg='+input,
	function(data){
	    $('#chatbox').text($('#chatbox').text()+'> '+input+'\n'+data+'\n');
      },'text');
});
});