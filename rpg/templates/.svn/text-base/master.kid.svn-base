<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?python import sitetemplate ?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="sitetemplate">

<head py:match="item.tag=='{http://www.w3.org/1999/xhtml}head'" py:attrs="item.items()">
    <meta content="text/html; charset=UTF-8" http-equiv="content-type" py:replace="''"/>
    <title py:replace="''">Your title goes here</title>
    <meta py:replace="item[:]" name="description" content="master template"/>
    <link rel="stylesheet" type="text/css" media="screen" href="../static/css/style.css"
        py:attrs="href=tg.url('/static/css/style.css')"/>
</head>

<body py:match="item.tag=='{http://www.w3.org/1999/xhtml}body'" py:attrs="item.items()">
    <div id="container">
    <div id="header">
		<h1>FighterMan</h1>
		<div id="img_bg"></div>
		<div id="img"></div>
    </div>
	
    <div py:if="not tg.identity.anonymous" id="nav">
	<a href="${tg.url('/home')}" title="Check stats and feed">Home</a> |
	<a href="${tg.url('/gym')}" title="Equip gear and train &quot; ${tg.identity.user.fighter.name} &quot;">Gym</a> |
	<a href="${tg.url('/shop')}" title="Buy and Sell Equipment">Shop</a> |
	<a href="${tg.url('/auction')}" title="Auction iff your unneeded stuff">Auction</a> |
	<a href="${tg.url('/arena')}" title="Challenge other Fighters">Arena</a> |
	<a href="${tg.url('/chat')}" title="Chat with other users">Chat</a> |
	<a href="${tg.url('/logout')}">Logout</a>
    </div>

    <div id="status_block" class="flash" py:if="value_of('tg_flash', None)" py:content="tg_flash"></div>
    <div py:replace="[item.text]+item[:]">page content</div>
    
    <div py:if="not tg.identity.anonymous" id="nav_float">
	<a class="img_roll_home" href="${tg.url('./home')}" title="Check stats and feed"></a>
	<a class="img_roll_gym" href="${tg.url('/gym')}" title="Equip gear and train &quot; ${tg.identity.user.fighter.name} &quot;"></a>
	<a class="img_roll_shop" href="${tg.url('/shop')}" title="Buy and Sell Equipment"></a>
	<a class="img_roll_auction" href="${tg.url('/auction')}" title="Auction iff your unneeded stuff"></a>
	<a class="img_roll_arena" href="${tg.url('/arena')}" title="Challenge other Fighters"></a>
	<a class="img_roll_chat" href="${tg.url('/chat')}" title="Chat with other users"></a>
    </div>
    </div>
</body>

</html>
