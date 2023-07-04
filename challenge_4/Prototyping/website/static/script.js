// ---------Responsive-navbar-active-animation-----------
function test() {
  var tabsNewAnim = $("#navbarSupportedContent");
  var activeItemNewAnim = tabsNewAnim.find(".active");
  var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
  var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
  var itemPosNewAnimTop = activeItemNewAnim.position();
  var itemPosNewAnimLeft = activeItemNewAnim.position();

  $(".hori-selector").css({
    top: itemPosNewAnimTop.top + "px",
    left: itemPosNewAnimLeft.left + "px",
    height: activeWidthNewAnimHeight + "px",
    width: activeWidthNewAnimWidth + "px",
  });
}

$(document).ready(function () {
  test();

  $("#navbarSupportedContent").on("click", "li", function (e) {
    e.preventDefault();

    // Remove active class from all nav items
    $("#navbarSupportedContent ul li").removeClass("active");

    // Add active class to the clicked nav item
    $(this).addClass("active");

    // Update the hori-selector position and size
    var activeWidthNewAnimHeight = $(this).innerHeight();
    var activeWidthNewAnimWidth = $(this).innerWidth();
    var itemPosNewAnimTop = $(this).position();
    var itemPosNewAnimLeft = $(this).position();

    $(".hori-selector").css({
      top: itemPosNewAnimTop.top + "px",
      left: itemPosNewAnimLeft.left + "px",
      height: activeWidthNewAnimHeight + "px",
      width: activeWidthNewAnimWidth + "px",
    });

    // Load the content based on the href of the clicked nav item
    var url = $(this).find("a").attr("href");
    loadContent(url);
  });
});

function loadContent(url) {
  // Hide the navbar and content section
  $("#navbarSupportedContent, #content-section").hide();

  $.ajax({
    url: url,
    type: "GET",
    dataType: "html",
    success: function (response) {
      if (url === "ferry73.html") {
        // Only update the content section without loading the navbar and footer
        var $contentSection = $("<div>")
          .html(response)
          .find("#content-section")
          .html();
        $("#content-section").html($contentSection);
      } else {
        // Update the entire content section including the navbar and footer
        $("#content-section").html(response);
      }

      // Slide the content section from the right
      $("#content-section").css("left", "100%");
      $("#content-section")
        .show()
        .animate({ left: "0" }, "slow", function () {
          // Show the navbar after the content section is fully shown
          $("#navbarSupportedContent").show();
          test();

          // Reset the position of the content section
          $("#content-section").css("left", "");
        });
    },
    error: function (xhr, status, error) {
      alert("Error loading the content.");
    },
  });
}

