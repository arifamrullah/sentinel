/*
 *
 *   INSPINIA - Responsive Admin Theme
 *   version 2.6
 *
 */


$(document).ready(function () {


    // Add body-small class if window less than 768px
    if ($(this).width() < 769) {
        $('body').addClass('body-small')
    } else {
        $('body').removeClass('body-small')
    }

    // MetsiMenu
    $('#side-menu').metisMenu();

    // Collapse ibox function
    $('.collapse-link').on('click', function () {
        var ibox = $(this).closest('div.ibox');
        var button = $(this).find('i');
        var content = ibox.find('div.ibox-content');
        content.slideToggle(200);
        button.toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
        ibox.toggleClass('').toggleClass('border-bottom');
        setTimeout(function () {
            ibox.resize();
            ibox.find('[id^=map-]').resize();
        }, 50);
    });

    // Close ibox function
    $('.close-link').on('click', function () {
        var content = $(this).closest('div.ibox');
        content.remove();
    });

    // Fullscreen ibox function
    $('.fullscreen-link').on('click', function () {
        var ibox = $(this).closest('div.ibox');
        var button = $(this).find('i');
        $('body').toggleClass('fullscreen-ibox-mode');
        button.toggleClass('fa-expand').toggleClass('fa-compress');
        ibox.toggleClass('fullscreen');
        setTimeout(function () {
            $(window).trigger('resize');
        }, 100);
    });

    // Close menu in canvas mode
    $('.close-canvas-menu').on('click', function () {
        $("body").toggleClass("mini-navbar");
        SmoothlyMenu();
    });

    // Run menu of canvas
    $('body.canvas-menu .sidebar-collapse').slimScroll({
        height: '100%',
        railOpacity: 0.9
    });

    // Open close right sidebar
    $('.right-sidebar-toggle').on('click', function () {
        $('#right-sidebar').toggleClass('sidebar-open');
    });

    // Initialize slimscroll for right sidebar
    $('.sidebar-container').slimScroll({
        height: '100%',
        railOpacity: 0.4,
        wheelStep: 10
    });

    // Open close small chat
    $('.open-small-chat').on('click', function () {
        $(this).children().toggleClass('fa-comments').toggleClass('fa-remove');
        $('.small-chat-box').toggleClass('active');
    });

    // Initialize slimscroll for small chat
    $('.small-chat-box .content').slimScroll({
        height: '234px',
        railOpacity: 0.4
    });

    // Small todo handler
    $('.check-link').on('click', function () {
        var button = $(this).find('i');
        var label = $(this).next('span');
        button.toggleClass('fa-check-square').toggleClass('fa-square-o');
        label.toggleClass('todo-completed');
        return false;
    });

    // Minimalize menu
    $('.navbar-minimalize').on('click', function () {
        $("body").toggleClass("mini-navbar");
        SmoothlyMenu();

    });

    // Tooltips demo
    $('.tooltip-demo').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body"
    });


    // Full height of sidebar
    function fix_height() {
        var heightWithoutNavbar = $("body > #wrapper").height() - 61;
        $(".sidebard-panel").css("min-height", heightWithoutNavbar + "px");

        var navbarHeigh = $('nav.navbar-default').height();
        var wrapperHeigh = $('#page-wrapper').height();

        if (navbarHeigh > wrapperHeigh) {
            $('#page-wrapper').css("min-height", navbarHeigh + "px");
        }

        if (navbarHeigh < wrapperHeigh) {
            $('#page-wrapper').css("min-height", $(window).height() + "px");
        }

        if ($('body').hasClass('fixed-nav')) {
            if (navbarHeigh > wrapperHeigh) {
                $('#page-wrapper').css("min-height", navbarHeigh + "px");
            } else {
                $('#page-wrapper').css("min-height", $(window).height() - 60 + "px");
            }
        }

    }

    fix_height();

    // Fixed Sidebar
    $(window).bind("load", function () {
        if ($("body").hasClass('fixed-sidebar')) {
            $('.sidebar-collapse').slimScroll({
                height: '100%',
                railOpacity: 0.9
            });
        }
    });

    // Move right sidebar top after scroll
    $(window).scroll(function () {
        if ($(window).scrollTop() > 0 && !$('body').hasClass('fixed-nav')) {
            $('#right-sidebar').addClass('sidebar-top');
        } else {
            $('#right-sidebar').removeClass('sidebar-top');
        }
    });

    $(window).bind("load resize scroll", function () {
        if (!$("body").hasClass('body-small')) {
            fix_height();
        }
    });

    $("[data-toggle=popover]")
        .popover();

    // Add slimscroll to element
    $('.full-height-scroll').slimscroll({
        height: '100%'
    })
});


// Minimalize menu when screen is less than 768px
$(window).bind("resize", function () {
    if ($(this).width() < 769) {
        $('body').addClass('body-small')
    } else {
        $('body').removeClass('body-small')
    }
});

// Local Storage functions
// Set proper body class and plugins based on user configuration
$(document).ready(function () {
    if (localStorageSupport()) {

        var collapse = localStorage.getItem("collapse_menu");
        var fixedsidebar = localStorage.getItem("fixedsidebar");
        var fixednavbar = localStorage.getItem("fixednavbar");
        var boxedlayout = localStorage.getItem("boxedlayout");
        var fixedfooter = localStorage.getItem("fixedfooter");

        var body = $('body');

        if (fixedsidebar == 'on') {
            body.addClass('fixed-sidebar');
            $('.sidebar-collapse').slimScroll({
                height: '100%',
                railOpacity: 0.9
            });
        }

        if (collapse == 'on') {
            if (body.hasClass('fixed-sidebar')) {
                if (!body.hasClass('body-small')) {
                    body.addClass('mini-navbar');
                }
            } else {
                if (!body.hasClass('body-small')) {
                    body.addClass('mini-navbar');
                }

            }
        }

        if (fixednavbar == 'on') {
            $(".navbar-static-top").removeClass('navbar-static-top').addClass('navbar-fixed-top');
            body.addClass('fixed-nav');
        }

        if (boxedlayout == 'on') {
            body.addClass('boxed-layout');
        }

        if (fixedfooter == 'on') {
            $(".footer").addClass('fixed');
        }
    }
});

// check if browser support HTML5 local storage
function localStorageSupport() {
    return (('localStorage' in window) && window['localStorage'] !== null)
}

// For demo purpose - animation css script
function animationHover(element, animation) {
    element = $(element);
    element.hover(
        function () {
            element.addClass('animated ' + animation);
        },
        function () {
            //wait for animation to finish before removing classes
            window.setTimeout(function () {
                element.removeClass('animated ' + animation);
            }, 2000);
        });
}

function SmoothlyMenu() {
    if (!$('body').hasClass('mini-navbar') || $('body').hasClass('body-small')) {
        // Hide menu in order to smoothly turn on when maximize menu
        $('#side-menu').hide();
        // For smoothly turn on menu
        setTimeout(
            function () {
                $('#side-menu').fadeIn(400);
            }, 200);
    } else if ($('body').hasClass('fixed-sidebar')) {
        $('#side-menu').hide();
        setTimeout(
            function () {
                $('#side-menu').fadeIn(400);
            }, 100);
    } else {
        // Remove all inline style from jquery fadeIn function to reset menu state
        $('#side-menu').removeAttr('style');
    }
}

// Dragable panels
function WinMove() {
    var element = "[class*=col]";
    var handle = ".ibox-title";
    var connect = "[class*=col]";
    $(element).sortable(
        {
            handle: handle,
            connectWith: connect,
            tolerance: 'pointer',
            forcePlaceholderSize: true,
            opacity: 0.8
        })
        .disableSelection();
}

// my functions
function tutup(id){
  $("#chart" + id).remove();
  $("#watch" + id).html("");
}


function moveToChart(){
  var element = "#cardsStock, #chartsStock";
  var handle = ".dragdrop";
  var connect = ".joinData";
  $(element).sortable(
      {
          handle: handle,
          connectWith: connect,
          tolerance: 'pointer',
          forcePlaceholderSize: true,
          opacity: 0.8,
          stop: function(data, ui){
            var charts = '<div class="ibox-title" id="chart' + ui.item[0].id +
              '"><h5>' + ui.item[0].id +
              '</h5><div class="ibox-tools"><a onClick="tutup(this.id)" id="' +
              ui.item[0].id + '"><i class="fa fa-times"></i></a></div></div>'+
              '<div class="ibox-content">' + ui.item[0].id + '</div></div>';
              var kd = ui.item[0].id;

            var chart = '<div class="animated flipInY ibox no-margins" id="chart' + kd + '">' +
                            '<div class="ibox-title">' +
                              '<h5>'+ kd.replace("card","") +' Stock Chart</h5>' +
                              '<div class="ibox-tools">' +
                                '<a onClick="tutup(this.id)" id="' + ui.item[0].id + '">' +
                                  '<i class="fa fa-times"></i>' +
                                '</a>' +
                              '</div>' +
                            '</div>' +
                            '<div class="ibox-content no-padding">' +
                              '<div class="flot-chart m-t-lg" style="height: auto; padding-bottom:10px">' +
                                '<canvas id="xx" height="70"></canvas>' +
                              '</div>' +
                            '</div>' +
                        '</div>';

            if($("#watch" + ui.item[0].id).html() == ""){
              $("#chartsStock").prepend(chart);
              $("#watch" + ui.item[0].id).html("<i class='fa fa-eye'></i>");
              var lineData = {
                  labels: ["January", "February", "March", "April", "May", "June", "July"],
                  datasets: [
                      {
                          label: "Price",
                          backgroundColor: "rgba(26,179,148,0.5)",
                          borderColor: "rgba(26,179,148,0.7)",
                          pointBackgroundColor: "rgba(26,179,148,1)",
                          pointBorderColor: "#fff",
                          data: [48, 48, 60, 39, 56, 37, 30]
                      },
                      {
                          label: "VWAP",
                          backgroundColor: "rgba(220,220,220,0.5)",
                          borderColor: "rgba(220,220,220,1)",
                          pointBackgroundColor: "rgba(220,220,220,1)",
                          pointBorderColor: "#fff",
                          data: [65, 59, 40, 51, 36, 25, 40]
                      }
                  ]
              };

              var lineOptions = {
                  responsive: true
              };


              var ctx = document.getElementById("xx").getContext("2d");
              new Chart(ctx, {type: 'line', data: lineData, options:lineOptions});
            }
            $(element).sortable('cancel')
          }
      })
      .disableSelection();
}

// card stock

function cardClose(id){
  $("#card" + id).fadeOut('slow',function(){
    $("#card" + id).remove();
  });

}

// stock List
function interest(kode){
  if (kode.change.substr(0,1) == '-') {
    var color = 'red-bg';
  }else{
    var color = 'navy-bg';
  }

  var card = '<div class="animated flipInY stock-card widget '+ color +' p-lg text-center" id="card' + kode.stock + '">' +
    '<div class="dragdrop stock-box" style="padding:10px 0;">' +
      '<div class="stock-card-overlay">' +
        '<a onClick="cardClose(this.id)" id="'+ kode.stock +'" style="position:absolute; right:10px; top:0px; padding:0;margin:5px 10px">' +
          '<i class="fa fa-times fa-stack-1x stock-eye"></i>' +
        '</a>' +
        '<span class="fa-stack fa-lg"></span>' +
      '</div>' +
      '<h3 class="m-xs margin-bottom-20px">'+kode.stock+'</h3>' +
      '<small class="stats-label">' + kode.time + '</small>' +
      '<h1 class="font-bold no-margin"> ' + kode.price + ' </h1>' +
      '<small class="stats-label p-w-xs" style="font-size:15px">' +
        '<label>' + kode.change + '</label>' +
      '</small>' +
      '<small style="font-size:15px" class="stats-label">' +
        '<label>' + kode.prc +'</label>' +
      '</small>' +
      '<p style="position:absolute; right:0px; top:0px; padding:0;margin:0 10px" id="watch' + kode.stock +'"></p>' +
    '</div>' +
  '</div>';
  $("#cardsStock").prepend(card);
  $("#interest" + kode.stock).html('<i class="fa fa-star fa-stack-1x stock-eye"></i>');
}

function watchList(kode){
  var chart = '<div class="animated flipInY ibox no-margins" id="chart' + kode + '">' +
                  '<div class="ibox-title">' +
                    '<h5>'+ kode +' Stock Chart</h5>' +
                    '<div class="ibox-tools">' +
                      '<a onClick="tutup(this.id)" id="' + kode + '">' +
                        '<i class="fa fa-times"></i>' +
                      '</a>' +
                    '</div>' +
                  '</div>' +
                  '<div class="ibox-content no-padding">' +
                    '<div class="flot-chart m-t-lg" style="height: auto; padding-bottom:10px">' +
                      '<canvas id="xx" height="70"></canvas>' +
                    '</div>' +
                  '</div>' +
              '</div>';
  $("#chartsStock").prepend(chart);
  var lineData = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
          {
              label: "Price",
              backgroundColor: "rgba(26,179,148,0.5)",
              borderColor: "rgba(26,179,148,0.7)",
              pointBackgroundColor: "rgba(26,179,148,1)",
              pointBorderColor: "#fff",
              data: [48, 48, 60, 39, 56, 37, 30]
          },
          {
              label: "VWAP",
              backgroundColor: "rgba(220,220,220,0.5)",
              borderColor: "rgba(220,220,220,1)",
              pointBackgroundColor: "rgba(220,220,220,1)",
              pointBorderColor: "#fff",
              data: [65, 59, 40, 51, 36, 25, 40]
          }
      ]
  };

  var lineOptions = {
      responsive: true
  };


  var ctx = document.getElementById("xx").getContext("2d");
  new Chart(ctx, {type: 'line', data: lineData, options:lineOptions});
}
