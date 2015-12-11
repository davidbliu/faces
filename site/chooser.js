var points = [];
var imname = 'me.jpg'
function savePoints(points){
  ptString = [];
  _.each(points, function(pt){
    ptString.push('['+pt.y+','+pt.x+']');
  });
  ptString = '['+ptString.join(',')+']';
  imRoot = imname.split('.')[0];
  alert(ptString + ' will be saved for '+imRoot);
  //save data using php
  var data = new FormData();
  data.append('data', ptString);
  data.append('imRoot', imRoot);
  var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
  xhr.open( 'post', './savePoints.php', true );
  xhr.send(data);
}

$(document).ready(function() {
  $("#save-btn").click(function(){
  console.log('saving points');
  savePoints(points);
  });
  function Point(x, y) {
    this.x = x;
    this.y = y;
  }
  function addPoint(point) {
    for (var i = 0; i < points.length; i++) {
      if (points[i] == null) {
        points[i] = point;
        return i;
      }
    }
    points.push(point);
    return points.length - 1;
  }
  function addPointHtml(point) {
    var point_i = addPoint(point);
    var point_html = $("<div></div>");
    point_html.addClass("point");
    point_html.css({left: point.x, top: point.y});
    point_html.text(point_i + 1);
    point_html.data("point_i", point_i);
    point_html.click(function() {
      var point_i = parseInt($(this).data("point_i"));
      points[point_i] = null;
      $(this).remove();
    });
    $("#container").append(point_html);
  }
  function destroyPoints() {
    points = [];
    $(".point").remove();
  }
  function loadImage(src) {
    $("#image").attr("src", './uploads/'+src);
  }
  function dumpPoints() {
    var points_data = [];
    for (var i = 0; i < points.length; i++) {
      if (points[i] != null) {
        points_data.push([points[i].x, points[i].y]);
      }
    }
    var points_json = JSON.stringify(points_data);
    $("#output-points").val(points_json);
  }
  $("#input-image").change(function() {
    imname = $(this).val();
    loadImage(imname);
  });
  $("#input-points-load").click(function() {
    destroyPoints();
    var points_data = JSON.parse($("#input-points").val());
    for (var i = 0; i < points_data.length; i++) {
      addPointHtml(new Point(points_data[i][0], points_data[i][1]));
    }
  });
  var line_vertical = document.getElementsByClassName("line-vertical")[0];
  var line_horizontal = document.getElementsByClassName("line-horizontal")[0];
  $("#image").click(function(event) {
    var x = event.offsetX;
    var y = event.offsetY;
    addPointHtml(new Point(x, y));
  });
  document.getElementById("image").addEventListener("mousemove", function(event) {
    var x = event.offsetX;
    var y = event.offsetY;
    line_vertical.style.left = x + "px";
    line_horizontal.style.top = y + "px";
  });
  $("#output-points-dump").click(function() {
    dumpPoints();
  });
  $("#make-lines-black").click(function() {
    $(".line-horizontal,.line-vertical").css("border-color", "black");
  });
  $("#make-lines-white").click(function() {
    $(".line-horizontal,.line-vertical").css("border-color", "white");
  });
  $("#input-image").val(imname).trigger("change");
});
