<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <meta http-equiv="Pragma" content="no-cache" />
    <title>FighterMan - Chat</title>

    <style media="screen" type="text/css">		
		#messages {
			height: 300px;
			overflow: auto;
			background-color: white;
			border: solid #000000 thin;
			padding: 5px;
		}
		
		#firstmessage {
			font-family: "Courier New", Courier, monospace;
			margin-top: 0px;
		}
	
		#firstuser {
			font-family: "Courier New", Courier, monospace;
			margin-top: 0px;
		}
	
		#users {
			float: right;
			height: 300px;
			overflow: auto;
			background-color: white;
			border: solid #000000 thin;
			padding: 5px;
		}
	
		#userlist ul {
			margin-left: 0;
			padding-left: 1em;
			text-indent: .1em;
		}
	
		#msg {
			width: 90%;
		}
		
		#data {
			width: 90%;
		}
	
		.msg_user {
			font-weight: bold;
		}
	
		.msg_date {
			
			font-size: 10px;
		}
		
		.msg_private {
			color: #FF6633;
		}
	
		.floatRight {
			float: right;
		}

    </style>

    <script type="text/javascript">
        var num = 0;
        getMessages();
        getUsers();

        function getMessages() {
                var d = loadJSONDoc('${tg.url("/getChat")}', {'tg_format':'json', 'num': num, 'room':'${room}'});
                d.addCallback(showMessages);
                setTimeout("getMessages()", 1000);
        }

        function showMessages(result) {
            if (result["msgs"].length > 0) {
                var msgs = map(extract, result["msgs"]);
                appendChildNodes("messages", msgs);
                var obj = getElement('messages');
                obj.scrollTop = obj.scrollHeight;
            }
        }

        function extract(msg) {
            if (msg["id"] > num) {
                num = msg["id"];
            }
			if (msg["target"] == "") {
	    		p = P({});
			} else {
				p = P({'class':'msg_private'}, "");
			}
			appendChildNodes(p, SPAN({'class':'msg_date'}, "[", toISOTime(isoTimestamp(msg["time"])),  "] "));
			appendChildNodes(p, SPAN({'class':'msg_user'}, msg["user"], ": "));
			appendChildNodes(p, SPAN({'class':'msg_msg'}, msg["message"]));
			return p;
        }
		
		function keyHandle(e) {
			var keynum;
			if (window.event) { // IE
				keynum = e.keyCode;
			} else if (e.which) { // Netscape/Firefox/Opera
				keynum = e.which;
			}
			if (keynum == 13) {
				sendMsg();
			}
		}
		
		function sendMsg() {
            var msg = getElement("msg");
			if (msg.value.trim() != "") {
				var d = doSimpleXMLHttpRequest("${tg.url('/saveChat')}", {'msg':msg.value, 'room':'${room}'});
				d.addCallback(function (result)
					{
						if (msg.value.substring(0, 5) == "/join") {
						location.reload(true);
					}
						msg.value = '';
						msg.focus();
					});
			}
        }

        function getUsers() {
			var d = loadJSONDoc('${tg.url("/getActiveUsers")}', {'tg_format':'json', 'room':'${room}'});
            d.addCallback(showUsers);
			setTimeout("getUsers()", 5000);
        }

		function showUsers(result) {
            var usrs = UL(null, map(extractUsers, result["users"]));
            replaceChildNodes("userlist", usrs);
        }

        function extractUsers(msg) {
            return LI(null, msg);
        }
		
		String.prototype.trim = function () {
    		return this.replace(/^\s*/, "").replace(/\s*$/, "");
		}
	</script>
</head>

<body>
	<h1 id="title_chat">Chat</h1>
	<div id="users">
	    <h3 id="firstuser">Users in '${room}':</h3>
	    <div id="userlist"></div>
	</div>

	<div id="messages">
	    <p id="firstmessage">Welcome to the '${room}' channel.</p>
	</div>
	<input type="text" name="msg" id="msg" onkeyup="javascript:keyHandle(event);" />
        <input type="button" name="submit" value="Send" onclick="javascript:sendMsg();"/>

	<h2><em>Instructions:</em></h2>
	<p><strong>Create channels on the fly:</strong> Use '/join channelName' to join a new or existing channel</p>
	<p><strong>Message individual users:</strong> Use '/msg userName message' to send a private message to a user</p>

</body>
<script type="text/javascript">
		getElement("msg").focus();
</script>
</html>
