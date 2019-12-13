
function openInNewTab(url) {
    var win = window.open(url, '_blank');
    win.focus();
  }
  function hide_capteha() {
    if ($("#capteha_modal").css('display') == 'block') {
      if ($('#timer').text() == "Alert - Non-elf detected!") {
        $( "#capteha_modal" ).fadeOut(100, function(){
          $('#capteha_modal_submit').css('display','block');
          $('.selected').removeClass('selected');
          $('.correctImage').removeClass('correctImage');
          $('.incorrectImage').removeClass('incorrectImage');
          $('.reCAPTEHAimages').remove();
        });
      }
    }
  }
  function non_elf_alert(){
    $('#capteha_modal_submit').css('display','none');
    $('#timer').css('color','#ff1a1a');
    $('#timer').css('font-size','3h');
    $('#timer').text('Alert - Non-elf detected!');
  }
  
  function decrement(){
    if ($("#capteha_modal").css('display') == 'block') {
      var time = parseInt($('#timer').text())-1;
      $('#timer').text(time);
      if (time>0) {
        setTimeout(function(){
          decrement()
        },1000);
      } else {
        non_elf_alert();
        setTimeout(function(){
          hide_capteha()
        },1000);
      } 
    }
  }
  function build_images(data) {
    var html="";
    for (var i=0; i<data.images.length; i++) {
      html += '<img height="auto" id="'+data.images[i].uuid+'" src="data:image/png;base64,'+data.images[i].base64+'" class="reCAPTEHAimages"/>'
    }
    $('#capteha_modal_images').html(html);
    $('#imagetype').text(data.select_type);
  }
  function submit_answers(answers=''){
    $.post( "api/capteha/submit", { 'answer': answers }, function( data ) {
      if (data.request) {
        $('#box-1').prop( "checked", true );
        hide_capteha()
      } else if ( answers != '' ) {
        non_elf_alert()
        var image_type = $('#imagetype').text();
        //var correct_images = data.data.filter(obj => {
        //  return obj.type === image_type
        //})
        //var correct_images = data.data.split(',');
        //$('#capteha_modal_submit').css('display','none');
        //for (var i=0; i < correct_images.length; i++) {
          //$('#'+correct_images[i].uuid).addClass('correctImage');
        //  $('#'+correct_images[i]).addClass('correctImage');
        //}
        //var selectect = $('.selected')
        //for (var i=0; i < selectect.length; i++) {
        //  if (!$(selectect[i]).hasClass('correctImage')) {
        //    $(selectect[i]).addClass('incorrectImage');
        //  }
        //}
        setTimeout(function(){
          hide_capteha()
        },1000);
      }
    })
  }
  function open_capteha() {
    setTimeout(function(){
      if ($("#capteha_modal").css('display') == 'none' && !$('#box-1').prop('checked')) {
        $('#imagetype').text('');
        $('#timer').css('color','black');
        $('#timer').text('5');
        $('#timer').css('font-size','3.5vh');
        var p = $( "#reCAPTEHA_parent" );
        var position = p.position();
        $('#capteha_modal').css({
          'position':'absolute',
          'top':position.top-$('#capteha_modal').height()-20,
          'left':position.left
        });
        $( "#capteha_modal" ).fadeIn(500, function(){
          var left = $(document).outerWidth() - $(window).width();
          $('body, html').scrollLeft(left);
          $("html, body").scrollTop($('#capteha_modal').offset().top);
        });
        $.post( "api/capteha/request", function( data ) {
          build_images(data);
        }).done(function(){
          setTimeout(function(){
            decrement()
          },1000);
        }).fail(function(){
            window.location.href = "/";
        });
      }
    },100);
  }
  
  $( document ).ready(function() {
      submit_answers();
      $('#capteha_modal_submit').click(function(){
          var selected_images = $('.selected');
          if (selected_images.length) {
              var ids = selected_images.map(function () {
                  return this.id;
              }).get().join(',');
              submit_answers(ids)
          }
      });
      $('#box-1').click(function(e){
          e.preventDefault();
          open_capteha();
      });
      $(document).on('click','.reCAPTEHAimages',function(){
          if ($(this).hasClass('selected')) {
              $(this).removeClass('selected');
          } else {
              $(this).addClass('selected');
          }
      });
  });