var express = require('express')
//, routes    = require('./routes')
, io  = require('socket.io').listen({{app_server_port}})
, twitter   = require('ntwitter')
, util      = require('util')
, twitterModule = require('./modules/twitterModule.js');

io.sockets.on('connection', function(socket){
  var twit = twitterModule.twit;
  twit.stream('statuses/filter', {'locations':'-180,-90,180,90'},
    function(stream){
      stream.on('data', function(data){
        socket.emit('twitter', strencode(data));
      });
    });
});

function strencode(data){
  return unescape(encodeURIComponent(JSON.stringify(data)));
}
