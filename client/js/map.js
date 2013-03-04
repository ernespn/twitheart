    var socket = io.connect('http://{{SERVER_NAME}}');
    var map = d3.geo.mercator();
    var path = d3.geo.path().projection(map);
    var n = 1000; //number of twitts showed
    var twitts = generateArray(n); //generate initial sets of data, TODO: generate from Memcache

    var width = 960, height = 500, zoom =2.2; 
    var lattop = 37, lonleft =-5, lonright =-3 ; //center map in Malaga

    centerIn(lattop, lonleft, lonright, zoom);
    refresh();
    
    socket.on('twitter', function(data){
      var datacured = strdecode(data);
      if (datacured.coordinates != null){
        var coordinatesmap = map([datacured.coordinates.coordinates[0], datacured.coordinates.coordinates[1]]);
        newdata([coordinatesmap[0], coordinatesmap[1]]);
      }
    });
    
    function centerIn(lat, lonl, lonr, zoom){
      var scale = zoom*width/(lonr-lonl);
      map.scale(scale);
      map.translate([0,0]);
      var trans = map([lonl, lat]);
      map.translate([-1*trans[0]+(width/2), -1*trans[1]+(height/2)]);
    }

    function refresh(){
      d3.json("world-countries.json", function(collection){
          //adding the map  
          d3.select("svg").selectAll("path").data(collection.features).enter()
            .append("path").attr("d", path).attr("fill", "#ccc")
            //function to test mouse over
            .on("mouseover", function(d){
              d3.selectAll(".active").classed("active", false);
              d3.select(d3.event.target).classed("active", true);})
            //adding the title
            .append("svg:title").text(function(d){ return d.properties.name});
          //adding the initial circles data
          d3.select("svg").selectAll("circle").data(twitts).enter()
            .append("circle");
        });
     }
     
     function redraw(){
        //update
        d3.select("svg").selectAll("circle")
          .data(twitts)
          .attr("cx", function(d,i){return d[0];})
          .attr("cy", function(d,i){return d[1];})
          .attr("r", 2)
          .attr("color", "red")
          .attr("circleid", function(d,i){return i;});
     }

     function newdata(value){
        //delete old one
        twitts.shift();
        //push new value
        twitts.push(value);
        //redraw circles
        redraw();
     }
    
    function drawPoint(x, y, r, color, opacity, text){
        var svg = d3.select("svg");
       // svg.selectAll("circle").data("twitts").enter()
        svg.append("circle")
          .attr("cx", x).attr("cy", y).attr("r", r)
          .style("fill", color).style("opacity", opacity)
          .append("title").text(text);
    }
    
    function generateArray(n){
        var arr = [];
        for(i=0; i<n; i++){
          arr[i] = [0,0];
        }
        return arr;
    }

    function strdecode(data){
        return JSON.parse(decodeURIComponent(escape(data)));
    }


